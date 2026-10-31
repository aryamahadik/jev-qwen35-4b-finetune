"""T60 CONTROL-NEXT -- SOLVER A (gold inside the generator; reads the structured record, never the rendered prompt).

Implements G0-lite T60 sections 3.2-3.4 with the Opus batch-1b rulings (T60-M1, M2, B1..B11):
  H1 DELEGATE-OR-DO   DELEGATE iff SIZE and BRIEF and BOUND and FREE (card numbers S_min, V, B_max, R_max are visible).
  H3 PLAN-OR-ACT      PLAN iff R1 (some step is IRREV: the shared D3 definition, written here independently of T59's code, T60-B11) and
                      R2 (at least n_min steps) and R3 (at least one ordering dependency of the DAG is NOT stated in the request).
  H2 KEEP-OR-DROP     KEEP iff a todo step on the unconditional plan takes the quoted fact from the CONTEXT, where `needs` is read by the
                      REFERENCE GRAMMAR (L1 handle, L2 role description, L3 ordinal, L4 chain / pointer); a fact superseded by a later
                      fact with the same role handle is not needed (the current value is); a done step does not count; the content of a
                      persisted artifact is not needed when a todo step reads the artifact from its pointer; under card k01 the steps that
                      only run on failure (rollback, retry, read-back) hosted by a todo step COUNT, under k02 they do not.
Nothing here executes anything.
"""
import posixpath

H1_LABELS = ("DELEGATE", "DO_HERE")
H2_LABELS = ("KEEP", "DROP")
H3_LABELS = ("PLAN", "ACT")


class SpecError(ValueError):
    pass


# ---- the shared irreversibility definition (G0-lite T59 D3 as amended by T59-M2), implemented independently of T59 ---------------------
def irrev(e, H):
    """e = {kind, backup, undo: None | {remaining}, external, magnitude, created_by_agent}."""
    if e["kind"] == "read":
        return False
    if e.get("magnitude", 0) >= H:
        return True
    if e.get("external"):
        return True
    if e["kind"] == "create" and e.get("created_by_agent"):
        return False
    undo = e.get("undo")
    return not (e.get("backup") or (undo is not None and undo.get("remaining", 0) >= 1))


# ======================================================================================================================
# H1
# ======================================================================================================================
def norm_path(p):
    """Paths are compared after collapsing ./ and ../ segments (an alias of a resource IS the resource)."""
    return posixpath.normpath(p)


def h1_predicates(sc):
    card, b, main = sc["card"], sc["brief"], sc["main"]
    steps = len(b["steps"])
    volume = sum(f["tokens"] for f in b["files"])
    main_touch = set()
    pend_writes = set()
    for m in main["pending"]:
        main_touch |= {norm_path(x) for x in list(m["reads"]) + list(m["writes"])}
        pend_writes |= {norm_path(x) for x in m["writes"]}
    shared = any(norm_path(w) in main_touch for w in b["writes"])
    # FREE also fails when the subtask reads a file that a pending main step still has to write (the declared output of a pending step feeds it)
    fed = bool(b["incoming"]) or any(norm_path(f["path"]) in pend_writes for f in b["files"])
    return dict(
        size=(steps >= card["S_min"] or volume >= card["V"]),
        brief=(len(b["needs"]) <= card["B_max"]),
        bound=(b["result_tokens"] <= card["R_max"]),
        free=(not shared and not fed),
        steps=steps, volume=volume, n_needs=len(b["needs"]), result=b["result_tokens"], shared_write=shared, pending_dep=fed)


def h1_label(sc):
    p = h1_predicates(sc)
    return "DELEGATE" if (p["size"] and p["brief"] and p["bound"] and p["free"]) else "DO_HERE"


# ======================================================================================================================
# H3
# ======================================================================================================================
def _closure(edges):
    reach = {}
    for a, b in edges:
        reach.setdefault(a, set()).add(b)
    changed = True
    while changed:
        changed = False
        for a in list(reach):
            for b in list(reach[a]):
                add = reach.get(b, set()) - reach[a]
                if add:
                    reach[a] |= add
                    changed = True
    return {(a, b) for a, bs in reach.items() for b in bs}


def h3_predicates(sc):
    """R3: some ordering dependency of the DAG is not implied by the order statements of the request (their transitive closure)."""
    card = sc["card"]
    steps = sc["steps"]
    r1 = any(irrev(s["effect"], card["H"]) for s in steps)
    r2 = len(steps) >= card["n_min"]
    implied = _closure([tuple(e) for e in sc["stated_edges"]])
    unstated = [e for e in sc["edges"] if tuple(e) not in implied]
    return dict(r1=r1, r2=r2, r3=bool(unstated), n_steps=len(steps), n_unstated=len(unstated))


def h3_label(sc):
    p = h3_predicates(sc)
    return "PLAN" if (p["r1"] and p["r2"] and p["r3"]) else "ACT"


# ======================================================================================================================
# H2: reference grammar, needs-set
# ======================================================================================================================
def fact_by_id(sc, fid):
    for f in sc["facts"]:
        if f["id"] == fid:
            return f
    raise SpecError("unknown fact %r" % fid)


def current_of(sc, f):
    """The current value of a role handle: the latest fact (highest transcript index) with the same handle and entity."""
    same = [x for x in sc["facts"] if x["handle"] == f["handle"] and x["entity"] == f["entity"] and x["type"] == f["type"]
            and x.get("art") == f.get("art")]
    return max(same, key=lambda x: x["idx"])


def resolve(sc, ref, steps_by_id):
    """-> set of fact ids the reference takes FROM THE CONTEXT (a chain adds what its deriving todo step takes)."""
    lv = ref["level"]
    if lv == 1:
        c = [f for f in sc["facts"] if f["handle"] == ref["handle"]]
        return {max(c, key=lambda x: x["idx"])["id"]} if c else set()
    if lv == 2:
        c = [f for f in sc["facts"] if f["entity"] == ref["entity"] and f["type"] == ref["ftype"]]
        return {max(c, key=lambda x: x["idx"])["id"]} if c else set()
    if lv == 3:
        rs = sorted([f for f in sc["facts"] if f["type"] == "R" and not f.get("content_of")], key=lambda x: x["idx"])
        k = ref["ordinal"]
        return {rs[k - 1]["id"]} if 1 <= k <= len(rs) else set()
    if lv == 4:
        if "via" in ref:                                   # the value a step derived: needs what that step takes, if it has not run
            u = steps_by_id[ref["via"]]
            if u["status"] == "done":
                return set()
            out = set()
            for r in u["refs"]:
                out |= resolve(sc, r, steps_by_id)
            return out
        if "pointer" in ref:                               # the saved location of an artifact: the pointer fact, never its content
            c = [f for f in sc["facts"] if f["type"] == "P" and f.get("art") == ref["pointer"]]
            return {c[0]["id"]} if c else set()
    raise SpecError("bad reference %r" % (ref,))


def needs(sc):
    """-> set of fact ids taken from the context by the steps that still run (todo, unconditional plan; under k01 also the hosted
    contingency steps of a todo host). Superseded facts map to the current value."""
    steps = {s["sid"]: s for s in sc["plan"]}
    out = set()
    counts_recovery = sc["card"].get("counts_recovery", False)
    for s in sc["plan"]:
        if s["status"] != "todo":
            continue
        if s.get("cond_host") is not None:
            host = steps[s["cond_host"]]
            if not (counts_recovery and host["status"] == "todo"):
                continue
        for r in s["refs"]:
            out |= resolve(sc, r, steps)
    return {current_of(sc, fact_by_id(sc, fid))["id"] for fid in out}


def h2_label(sc):
    q = fact_by_id(sc, sc["quote"])
    return "KEEP" if q["id"] in needs(sc) and current_of(sc, q)["id"] == q["id"] else "DROP"


def gold_label(rec):
    sc = rec["scene"]
    return {"h1": h1_label, "h2": h2_label, "h3": h3_label}[sc["head"]](sc)


# ======================================================================================================================
# plan readiness (K22 d): T60's own computation, compared by the G9 test with the T54 Kahn levels and a longest-path algorithm
# ======================================================================================================================
def h3_edges(sc):
    return [tuple(e) for e in sc["edges"]]


def h2_plan_edges(sc):
    """Dependency edges of an H2 plan: a step that takes 'the value derived in step u' waits for u; a contingency step waits for its host."""
    out = []
    for s in sc["plan"]:
        for r in s["refs"]:
            if r.get("level") == 4 and "via" in r:
                out.append((r["via"], s["sid"]))
        if s.get("cond_host"):
            out.append((s["cond_host"], s["sid"]))
    return out


def ready_steps(sc):
    """Steps that can be issued now: pending (not done) steps whose every dependency is done. H3: every step is pending."""
    if sc["head"] == "h3":
        nodes = [s["sid"] for s in sc["steps"]]
        edges = h3_edges(sc)
        done = set()
    else:
        nodes = [s["sid"] for s in sc["plan"]]
        edges = h2_plan_edges(sc)
        done = {s["sid"] for s in sc["plan"] if s["status"] == "done"}
    waiting = {n: {a for a, b in edges if b == n} for n in nodes}
    return sorted(n for n in nodes if n not in done and all(d in done for d in waiting[n]))
