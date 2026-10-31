"""T60 brute-force ORACLES (K3 cross-checks; they share no code with t60_rule):
  H1  a list of REASONS for doing it here; DELEGATE iff the list is empty.
  H3  irreversibility by SIMULATION on a one-cell world (apply the effect, try to put the cell back); the order dependency by
      ENUMERATING step orders: R3 holds iff the request admits an order that violates a DAG edge.
  H2  ABLATION: redact the quoted fact from the context, run the steps that would still run in a simulated state, and say KEEP iff a
      step fails for lack of it. References are resolved by looking facts up in the TRANSCRIPT order (a lookup index), not through the
      rule module's resolver.
"""
import itertools
import os


def h1_oracle(sc):
    c, b, main = sc["card"], sc["brief"], sc["main"]
    reasons = []
    vol = 0
    for f in b["files"]:
        vol += f["tokens"]
    if not (len(b["steps"]) >= c["S_min"] or vol >= c["V"]):
        reasons.append("small")
    if len(b["needs"]) > c["B_max"]:
        reasons.append("coupled")
    if b["result_tokens"] > c["R_max"]:
        reasons.append("big_result")
    for res in b["writes"]:
        for m in main["pending"]:
            if any(os.path.normpath(x) == os.path.normpath(res) for x in list(m["reads"]) + list(m["writes"])):
                reasons.append("shared")
    if b["incoming"]:
        reasons.append("pending")
    for f in b["files"]:                                  # the subtask reads a file that a pending main step still has to write
        for m in main["pending"]:
            if any(os.path.normpath(x) == os.path.normpath(f["path"]) for x in m["writes"]):
                reasons.append("fed")
    return "DO_HERE" if reasons else "DELEGATE"


def _cannot_be_taken_back(e, H):
    if e["kind"] == "read":
        return False
    cell = "after"
    if not e.get("external"):
        if e["kind"] == "create" and e.get("created_by_agent"):
            cell = "before"
        elif e.get("backup"):
            cell = "before"
        elif e.get("undo") is not None and e["undo"].get("remaining", 0) >= 1:
            cell = "before"
    return cell != "before" or e.get("magnitude", 0) >= H


def h3_oracle(sc):
    c = sc["card"]
    steps = sc["steps"]
    r1 = any(_cannot_be_taken_back(s["effect"], c["H"]) for s in steps)
    r2 = len(steps) >= c["n_min"]
    ids = [s["sid"] for s in steps]
    stated = [tuple(e) for e in sc["stated_edges"]]
    dag = [tuple(e) for e in sc["edges"]]
    r3 = False
    if len(ids) <= 8:
        for perm in itertools.permutations(ids):
            pos = {x: i for i, x in enumerate(perm)}
            if all(pos[a] < pos[b] for a, b in stated) and not all(pos[a] < pos[b] for a, b in dag):
                r3 = True
                break
    else:
        raise ValueError("oracle enumerates at most 8 steps")
    return "PLAN" if (r1 and r2 and r3) else "ACT"


def h2_oracle(sc):
    """KEEP iff redacting the quoted fact makes a step that would run fail."""
    quote = next(f for f in sc["facts"] if f["id"] == sc["quote"])
    counts = sc["card"].get("counts_recovery", False)
    by_sid = {s["sid"]: s for s in sc["plan"]}
    order = sorted(sc["facts"], key=lambda f: f["idx"])

    def current(f):
        later = [x for x in order if x["handle"] == f["handle"] and x["entity"] == f["entity"] and x["type"] == f["type"]
                 and x.get("art") == f.get("art") and x["idx"] > f["idx"]]
        return later[-1] if later else f

    def lookup(ref):
        lv = ref["level"]
        if lv == 1:
            hit = [f for f in order if f["handle"] == ref["handle"]]
        elif lv == 2:
            hit = [f for f in order if f["entity"] == ref["entity"] and f["type"] == ref["ftype"]]
        elif lv == 3:
            fetched = [f for f in order if f["type"] == "R" and not f.get("content_of")]
            hit = [fetched[ref["ordinal"] - 1]] if 0 < ref["ordinal"] <= len(fetched) else []
        elif "pointer" in ref:
            hit = [f for f in order if f["type"] == "P" and f.get("art") == ref["pointer"]]
        else:
            hit = []
        return [current(hit[-1])] if hit else []

    def step_fails(s, redacted_id):
        for ref in s["refs"]:
            if "via" in ref:
                u = by_sid[ref["via"]]
                if u["status"] == "todo" and step_fails(u, redacted_id):
                    return True
                continue
            if any(f["id"] == redacted_id for f in lookup(ref)):
                return True
        return False

    target = current(quote)
    if target["id"] != quote["id"]:
        return "DROP"
    for s in sc["plan"]:
        if s["status"] != "todo":
            continue
        if s.get("cond_host") is not None and not (counts and by_sid[s["cond_host"]]["status"] == "todo"):
            continue
        if step_fails(s, quote["id"]):
            return "KEEP"
    return "DROP"


def oracle_label(sc):
    return {"h1": h1_oracle, "h2": h2_oracle, "h3": h3_oracle}[sc["head"]](sc)
