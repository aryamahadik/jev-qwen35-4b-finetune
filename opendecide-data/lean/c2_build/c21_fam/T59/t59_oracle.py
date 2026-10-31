"""T59 brute-force ORACLE (G0-lite K3): an implementation of the plan rule that shares no code with t59_solver_a.

  * Interpretations are ENUMERATED from the slots' value lists (itertools.product) and looked up in the case's table, instead of
    filtering the table by the collapsed values.
  * Each candidate action is SIMULATED on a one-cell world: apply the effect, then try to restore the cell with the backup or the
    undo tool; the action is irreversible when the cell cannot be restored, or when the effect is large (magnitude >= H).
  * ROBUST is decided by trying every sufficient condition in turn on the enumerated readings.
  * The T6 3.3.1 sub-cases (Opus ruling Q2) are decided by SIMULATING the plain retry in both worlds (ambiguous write) and by asking whether
    the corrected value is available (invalid_named_arg), not by the solver-A boolean.
It is used by the truth-table test (full cross product of the plan rule's inputs) and as a second opinion in the gates.
"""
import itertools


def _fixed_values(case):
    """slot id -> the one value the slot is pinned to by what the user / card says, or None."""
    out = {}
    for s in case["slots"]:
        v = None
        if s.get("stated") is not None:
            v = s["stated"]
        elif s.get("default") is not None and case["defaults_count"]:
            v = s["default"]
        elif s.get("delegation"):
            v = s["pick"]
        elif s.get("winner") is not None:
            v = s["winner"]
        out[s["id"]] = v
    return out


def _lookup(case, assign):
    for i in case["interps"]:
        if i["assign"] == assign:
            return i
    return None


def _readings(case):
    fixed = _fixed_values(case)
    pools = []
    ids = []
    for s in case["slots"]:
        ids.append(s["id"])
        pools.append([fixed[s["id"]]] if fixed[s["id"]] is not None else list(s["values"]))
    out = []
    for combo in itertools.product(*pools):
        got = _lookup(case, dict(zip(ids, combo)))
        if got is not None:
            out.append(got)
    return out, fixed


def _cannot_be_taken_back(eff, H):
    """Apply the effect to a one-cell world, then try to put the cell back."""
    if eff["kind"] == "read":
        return False
    cell = "before"
    cell = "after"                                           # the effect happened
    external = bool(eff.get("external"))
    if not external:
        if eff["kind"] == "create" and eff.get("created_by_agent"):
            cell = "before"                                  # the agent removes what it made
        elif eff.get("backup"):
            cell = "before"                                  # restore from the backup
        else:
            u = eff.get("undo")
            if u is not None and u.get("remaining", 0) >= 1:
                cell = "before"                              # the undo tool, still inside its window
    return cell != "before" or eff.get("magnitude", 0) >= H


def _plain_retry_duplicates(first_write_committed, key, read_path):
    """Ambiguous write (timeout): one cell counts the writes. The agent's forward move is a retry; a key makes a repeated call a no-op, a read
    path lets it look first and skip the retry when the write landed."""
    writes = 1 if first_write_committed else 0
    if first_write_committed and (key or read_path):
        pass                                                 # the retry is skipped or absorbed
    else:
        writes += 1                                          # the plain retry
    return writes > 1


def _t6_forced_ask(case):
    """G0-lite 3.3.1 forced ASK, simulated: True when no forward move is safe in every world without asking."""
    d = case.get("t6")
    if d is None:
        return False
    if d["cls"] == "ambiguous":
        if d["read_path"] and not case["read_first"]:
            raise ValueError("oracle: read path listed without read_first")
        return any(_plain_retry_duplicates(w, d["key"], d["read_path"]) for w in (True, False))
    if d["cls"] == "invalid_named":
        return not d["corrected_in_ctx"]                     # the agent would have to invent the value
    raise ValueError("oracle: no 3.3.1 rule for T6 class %r" % d["cls"])


def _key(m):
    return "%s|%s|%s" % (m["g"], m["t"], ",".join("%s=%s" % (k, m["p"][k]) for k in sorted(m.get("p", {}))))


def oracle_label(case):
    if not case["forward"]:
        return "ASK"
    rd, fixed = _readings(case)
    if not rd:
        raise ValueError("oracle: no reading")
    per = [set(_key(m) for m in r["muts"]) for r in rd]
    distinct = {tuple(sorted(p)) for p in per}
    planned = set(_key(m) for m in case["planned"])
    robust = False
    if len(distinct) == 1:                                   # R-SAME: every reading leads to the same action
        robust = True
    if all(v is not None for v in fixed.values()):           # R-DEF: nothing is left open
        robust = True
    if planned and all(planned.issubset(p) for p in per):    # R-COM
        robust = True
    for s in case["slots"]:                                  # R-RES
        if fixed[s["id"]] is None and s["kind"] == "WORLD" and s.get("resolver") and case["read_first"]:
            robust = True
    if robust:
        return "PROCEED"
    if _t6_forced_ask(case):                                 # 3.3.1 binds on every card (Opus ruling Q2)
        return "ASK"
    if case["mode"] == "OFF":
        return "ASK"
    H = case["H"]
    for r in rd:
        for m in r["muts"]:
            if _cannot_be_taken_back(m["eff"], H):
                return "ASK"
    return "PROCEED"


# ---- case factory for the truth table -----------------------------------------------------------------------------------------
def eff_rec(irreversible, kind="delete"):
    return dict(kind=kind, backup=not irreversible, undo=None, external=False, magnitude=1, created_by_agent=False)


# T6 3.3.1 sub-cases of the truth table: name -> descriptor (None = not a T6 case). `forced` is the spec sentence, written out by hand.
T6_SUBCASES = {
    "none": (None, False),
    "amb_neither": (dict(cls="ambiguous", key=False, read_path=False, corrected_in_ctx=False), True),
    "amb_key": (dict(cls="ambiguous", key=True, read_path=False, corrected_in_ctx=False), False),
    "amb_read_path": (dict(cls="ambiguous", key=False, read_path=True, corrected_in_ctx=False), False),
    "amb_key_and_read_path": (dict(cls="ambiguous", key=True, read_path=True, corrected_in_ctx=False), False),
    "invalid_named_not_in_ctx": (dict(cls="invalid_named", key=False, read_path=False, corrected_in_ctx=False), True),
    "invalid_named_in_ctx": (dict(cls="invalid_named", key=False, read_path=False, corrected_in_ctx=True), False),
}


def case_from_flags(e_empty, r_same, collapsed, r_com, r_res, any_irrev, mode, H=10, t6=None):
    """A minimal consistent case with exactly these properties. Slot A (INTENT) has two values; B (WORLD) exists only when r_res or a
    second slot is wanted. `collapsed` pins slot A to its first value (and, when B exists for r_res, B stays open and resolver-backed)."""
    good, bad = eff_rec(False), eff_rec(any_irrev)
    slots = [dict(id="A", kind="INTENT", values=["a1", "a2"], stated="a1" if collapsed else None, default=None, delegation=False,
                  pick=None, winner=None, resolver=False)]
    if r_res:
        slots.append(dict(id="B", kind="WORLD", values=["w1", "w2"], stated=None, default=None, delegation=False, pick=None,
                          winner=None, resolver=True))
    else:
        slots.append(dict(id="B", kind="WORLD", values=["w1"], stated="w1", default=None, delegation=False, pick=None,
                          winner=None, resolver=False))
    mut_a1 = dict(g="g:act", t="x1", p={}, eff=good)
    mut_a2 = dict(g="g:act", t="x2", p={}, eff=bad)
    common = dict(g="g:act", t="x0", p={}, eff=good)
    interps = []
    for av in ("a1", "a2"):
        for bv in (["w1", "w2"] if r_res else ["w1"]):
            if r_same:
                muts = [dict(mut_a1)]
                if any_irrev and av == "a2":
                    muts = [dict(mut_a1, eff=bad)]
                if any_irrev and av == "a1":
                    muts = [dict(mut_a1, eff=bad)]
            else:
                muts = [dict(mut_a1)] if av == "a1" else [dict(mut_a2)]
            if r_com:
                muts = muts + [dict(common)]
            interps.append(dict(assign={"A": av, "B": bv}, muts=muts))
    planned = [dict(common)] if r_com else [dict(mut_a1)]
    if not r_com and r_same:
        planned = [dict(mut_a1)]
    # the plain 'any_irrev' flag must hold on the admissible readings even when A is collapsed to a1
    if any_irrev and not r_same:
        for i in interps:
            if i["assign"]["A"] == "a1" and collapsed:
                i["muts"] = [dict(m, eff=bad) if m["t"] == "x1" else m for m in i["muts"]]
    case = dict(mode=mode, H=H, defaults_count=False, read_first=bool(r_res) or bool(t6 and t6.get("read_path")), forward=not e_empty,
                slots=slots, interps=interps, planned=planned)
    if t6 is not None:
        case["t6"] = dict(t6)
    return case
