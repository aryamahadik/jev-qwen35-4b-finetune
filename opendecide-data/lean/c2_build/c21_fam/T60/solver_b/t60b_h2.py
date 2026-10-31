"""T60 solver B, head H2 KEEP-OR-DROP (G0_LITE sections 3.4 and 3.5, ROW_SCHEMA H2). String side + ABLATION.

Method (different from a needs-set computation): parse the rendered row into a context (transcript events -> facts), a plan (todo / done steps
with their references, contingency hosts) and the quoted fact. Resolve the reference grammar (L1 handle, L2 role description, L3 ordinal,
L4 chain or pointer) against the context. Then run the plan twice in a simulated state:
  * BASELINE: the full context;
  * ABLATED : the quoted fact is REDACTED (replaced by a hole; the turn structure is kept so that ordinals do not shift). A "reminder" turn
              that only restates the same fact is the same fact seen again, so it is redacted with it; a second, separate statement is not.
A step runs if it is todo and either unconditional or a contingency step of a todo host while the card counts recovery steps. A step FAILS
when one of its references resolves to a redacted fact (or to a failed step). KEEP iff some step runs in the baseline and fails in the ablated
run, i.e. the plan breaks for lack of the quoted fact. Nothing is executed beyond this in-process dictionary simulation.
Same-value supersession (a chain with a repeated value; a repeat marker on a revised fact) is outside the spec and ABSTAINS (Opus ruling Q1)."""
import re

try:
    from .t60b_text import ParseGap, Rx, lines_of, strip_notes
except ImportError:
    from t60b_text import ParseGap, Rx, lines_of, strip_notes

ORDINALS = ("first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth")
TYPE_WORDS = {"a value given by the user": ("V",), "a tool result": ("R", "C"), "a decision taken earlier": ("D",),
              "a state key": ("S",), "a saved location": ("P",)}

_RE_HEAD = Rx(r"^\((\d+)\)\s+(.*)$")
_RE_USER_V = Rx(r"^User:\s*The (\S+) for the (\S+) is (.+)\.$")
_RE_USER_D = Rx(r"^User:\s*Let us go with (.+?) as the (\S+) of the (\S+?)\.$")
_RE_USER_M = Rx(r"^User:\s*As a reminder, the (\S+) for the (\S+) is (.+)\.$")
_RE_CALL = Rx(r"^Agent called (get|create|export|read|check)_([^\s(]+)\((.*)\)\s*$")
_RE_KV = Rx(r"^\s*(\S+):\s*(.*\S)\s*$")
_RE_QUOTE = Rx(r"^(?:The f|F)act in question \(turn (\d+), ([^)]*)\):\s*(\S+):\s*(.*\S)\s*$")
_RE_STEP = Rx(r"^\[(done|todo)\]\s+step\s+(\d+)(?:\s+\(only if step\s+(\d+)\s+fails\))?:\s*(\S+)\s+the\s+(\S+?)(?:\s+using\s+(.+))?\s*$")
_RE_TRAIL_PAREN = Rx(r"\s*\([^()]*\)\s*$")


def _clean_value(v):
    v = v.strip()
    prev = None
    while prev != v:
        prev = v
        v = _RE_TRAIL_PAREN.sub("", v).strip()
    return v


# ----------------------------------------------------------------------------------------------------------------------
# parse
# ----------------------------------------------------------------------------------------------------------------------
def parse_counts_recovery(card_lines):
    for ln in card_lines:
        low = ln.lower()
        if not re.search(r"roll-?back|retry|read-back|only on failure|only run if|only runs when|fails|failure", low):
            continue
        if re.search(r"\b(do|does|did)\s+not\s+count\b|\bnot\s+counted?\b|\bnever\s+counts?\b|\bdon't\s+count\b|\bdoesn't\s+count\b", low):
            return False
        if re.search(r"\bcounts?\b", low):
            return True
        raise ParseGap("h2_recovery_clause")
    raise ParseGap("h2_recovery_clause_missing")


def parse_ref(text):
    """One reference of a plan step -> dict(level, ...). ParseGap for a shape outside the reference grammar."""
    t = text.strip()
    m = re.fullmatch(r"the value derived in step s?(\d+)", t)
    if m:
        return {"level": 4, "kind": "chain", "step": int(m.group(1))}
    m = re.fullmatch(r"the saved location of the (\S+) snapshot", t)
    if m:
        return {"level": 4, "kind": "pointer", "entity": m.group(1)}
    m = re.fullmatch(r"the (%s) record fetched by a get call" % "|".join(ORDINALS), t)
    if m:
        return {"level": 3, "ordinal": ORDINALS.index(m.group(1)) + 1}
    m = re.fullmatch(r"the value (given|returned|we agreed) for the (\S+)", t)
    if m:
        return {"level": 2, "ftype": {"given": "V", "returned": "R", "we agreed": "D"}[m.group(1)], "entity": m.group(2)}
    m = re.fullmatch(r"the key recorded for the (\S+)", t)
    if m:
        return {"level": 2, "ftype": "S", "entity": m.group(1)}
    m = re.fullmatch(r"the saved location for the (\S+)", t)
    if m:
        return {"level": 2, "ftype": "P", "entity": m.group(1)}
    m = re.fullmatch(r"the (\S+)", t)
    if m:
        return {"level": 1, "handle": m.group(1)}
    raise ParseGap("h2_reference_shape")


def parse_plan_line(ln):
    m = _RE_STEP.match(ln.strip())
    if not m:
        raise ParseGap("h2_plan_line")
    refs = []
    if m.group(6):
        for part in re.split(r"\s+and\s+", m.group(6).strip()):
            refs.append(parse_ref(part))
    return {"n": int(m.group(2)), "status": m.group(1), "host": int(m.group(3)) if m.group(3) else None, "verb": m.group(4),
            "entity": m.group(5), "refs": refs}


def parse_events(lines):
    """Transcript lines -> events, one per numbered turn, each with the facts it states."""
    evs = []
    for ln in lines:
        m = _RE_HEAD.match(ln)
        if m:
            evs.append({"turn": int(m.group(1)), "head": m.group(2).strip(), "body": []})
        elif ln.strip():
            if not evs:
                raise ParseGap("h2_transcript_orphan_line")
            evs[-1]["body"].append(ln)
    turns = [e["turn"] for e in evs]
    if turns != list(range(1, len(turns) + 1)):
        raise ParseGap("h2_turn_numbers")
    out = []
    for e in evs:
        h = e["head"]
        facts = []
        verb = None
        if h.startswith("User:"):
            m = _RE_USER_M.match(_clean_user(h))
            kind = "M"
            if not m:
                m = _RE_USER_V.match(_clean_user(h))
                kind = "V"
            if m:
                facts.append({"ftype": kind, "handle": m.group(1), "entity": m.group(2), "value": _clean_value(m.group(3))})
            else:
                m = _RE_USER_D.match(_clean_user(h))
                if not m:
                    raise ParseGap("h2_user_shape")
                facts.append({"ftype": "D", "handle": m.group(2), "entity": m.group(3), "value": _clean_value(m.group(1))})
        else:
            m = _RE_CALL.match(h)
            if not m:
                raise ParseGap("h2_event_shape")
            verb, ent = m.group(1), m.group(2)
            kvs = []
            seen_out = False
            for b in e["body"]:
                if b.strip().startswith("-> output:"):
                    seen_out = True
                    continue
                km = _RE_KV.match(b)
                if not seen_out or not km:
                    raise ParseGap("h2_output_line")
                kvs.append((km.group(1), _clean_value(km.group(2))))
            if verb != "check":
                if len(kvs) != 1:
                    raise ParseGap("h2_output_fields")
                ftype = {"get": "R", "create": "S", "export": "P", "read": "C"}[verb]
                if verb == "export" and kvs[0][0] != "path":
                    raise ParseGap("h2_pointer_key")
                facts.append({"ftype": ftype, "handle": kvs[0][0], "entity": ent, "value": kvs[0][1]})
        out.append({"turn": e["turn"], "verb": verb, "facts": facts})
    return out


def _clean_user(h):
    """'User: The x for the y is 4 (a notable value).' -> the same line with the emphasis parenthetical removed before the final dot."""
    s = h.strip()
    m = re.match(r"^(.*?)(\s*\([^()]*\))\.$", s)
    if m:
        return m.group(1) + "."
    return s


def parse(context):
    ls = strip_notes(lines_of(context))
    try:
        i_plan = next(i for i, ln in enumerate(ls) if ln.strip() == "Remaining plan:")
        i_tr = next(i for i, ln in enumerate(ls) if ln.strip() == "Context transcript:")
    except StopIteration:
        raise ParseGap("h2_sections_missing")
    if not (1 <= i_plan < i_tr):
        raise ParseGap("h2_sections_order")
    # the card is everything above the task statement; the task statement is the one line right above "Remaining plan:" (a cue wrapper, when
    # one is present, sits on that same line)
    counts = parse_counts_recovery(ls[:i_plan - 1])
    i_q = None
    for i in range(len(ls) - 1, i_tr, -1):
        if _RE_QUOTE.match(ls[i].strip()):
            i_q = i
            break
    if i_q is None:
        raise ParseGap("h2_quote_missing")
    plan = [parse_plan_line(ln) for ln in ls[i_plan + 1:i_tr] if ln.strip()]
    if not plan or [s["n"] for s in plan] != list(range(1, len(plan) + 1)):
        raise ParseGap("h2_plan_numbers")
    events = parse_events(ls[i_tr + 1:i_q])
    qm = _RE_QUOTE.match(ls[i_q].strip())
    quote = {"turn": int(qm.group(1)), "type_word": qm.group(2).strip(), "handle": qm.group(3), "value": _clean_value(qm.group(4))}
    return {"counts_recovery": counts, "plan": plan, "events": events, "quote": quote}


# ----------------------------------------------------------------------------------------------------------------------
# reference resolution and the ablation simulator
# ----------------------------------------------------------------------------------------------------------------------
def fact_table(events):
    """Flat list of facts in transcript order: dict(turn, ftype, handle, entity, value, verb). A 'reminder' turn that restates an earlier
    fact (same handle, entity and value) is the SAME fact seen again: it gets ftype 'M' and `alias_of` = the first mention's turn. A reminder
    with no such earlier fact is an ordinary stated value."""
    out = []
    for e in events:
        for f in e["facts"]:
            d = dict(f)
            d["turn"] = e["turn"]
            d["verb"] = e["verb"]
            if d["ftype"] == "M":
                first = [x for x in out if x["ftype"] != "M" and (x["handle"], x["entity"], x["value"]) == (d["handle"], d["entity"], d["value"])]
                if first:
                    d["alias_of"] = first[0]["turn"]
                else:
                    d["ftype"] = "V"
            out.append(d)
    return out


def check_no_same_value_supersession(allf):
    """Opus ruling Q1 (18 Oct). Same-value supersession is outside the spec: a chain (facts with the same handle and entity, in any type) whose
    values are not pairwise distinct, or a repeat-marker ('reminder') turn on a fact that has a revision in the transcript (the reminder is
    appended at the END, so it would repeat a value after its revision), has no unambiguous label. B does not label it: ParseGap -> abstain.
    `allf` = fact_table(...) (reminders included, as ftype 'M')."""
    chain = {}
    for f in allf:
        if f["ftype"] == "M":
            continue
        chain.setdefault((f["handle"], f["entity"]), []).append(f["value"])
    for key, vals in chain.items():
        if len(set(vals)) != len(vals):
            raise ParseGap("h2_same_value_supersession")
    for f in allf:
        if f["ftype"] == "M" and len(chain.get((f["handle"], f["entity"]), ())) >= 2:
            raise ParseGap("h2_repeat_marker_in_supersession_chain")


def quoted_fact(p, facts):
    q = p["quote"]
    at = [f for f in facts if f["turn"] == q["turn"]]
    if len(at) != 1:
        raise ParseGap("h2_quote_turn")
    f = at[0]
    if f["ftype"] == "M" or f["handle"] != q["handle"] or f["value"] != q["value"]:
        raise ParseGap("h2_quote_event_mismatch")
    if f["ftype"] not in TYPE_WORDS.get(q["type_word"], ()):
        raise ParseGap("h2_quote_type_mismatch")
    return f


def resolve(ref, step, facts, notes):
    """The fact a reference takes from the context, or None (nothing in the context answers it). `facts` excludes restated reminders."""
    lv = ref["level"]
    if lv == 1:
        c = [f for f in facts if f["handle"] == ref["handle"]]
        same = [f for f in c if f["entity"] == step["entity"]]
        c = same or c
    elif lv == 2:
        c = [f for f in facts if f["ftype"] == ref["ftype"] and f["entity"] == ref["entity"]]
        if ref["ftype"] == "R" and not c:
            c = [f for f in facts if f["ftype"] == "C" and f["entity"] == ref["entity"]]
        if len({f["handle"] for f in c}) > 1:
            notes.append("l2_multi_handle")
    elif lv == 3:
        gets = [f for f in facts if f["ftype"] == "R"]
        c = [gets[ref["ordinal"] - 1]] if ref["ordinal"] <= len(gets) else []
    elif ref["kind"] == "pointer":
        c = [f for f in facts if f["ftype"] == "P" and f["entity"] == ref["entity"]]
    else:
        raise ParseGap("h2_resolve_chain_here")
    if not c:
        return None
    f = c[-1]
    # A fact superseded by a later fact with the same role handle is not needed (the current value is) [G0-lite 3.4]; "a fact is replaced by the latest
    # fact with the same <handle> and <entity>" [ROW_SCHEMA]. That holds whichever level named the fact: an ordinal (L3) or a role description (L2) that
    # lands on a superseded record takes the CURRENT value of that role instead. (For L1 the latest fact is picked above already.)
    latest = [g for g in facts if g["handle"] == f["handle"] and g["entity"] == f["entity"]]
    return latest[-1] if latest else f


def run_plan(p, facts, redacted, notes):
    """-> {step number: 'ok' | 'fail'} for the steps that run. `redacted` is a set of fact ids (the turn of a fact's first mention).
    A step runs when it is todo and either unconditional or a contingency step of a todo host while the card counts recovery steps. It fails
    when one of its references resolves to a redacted fact. A chain reference (`the value derived in step K`) takes what step K takes when K is
    todo (whether or not K itself runs in this plan), and nothing when K is done (its value was derived earlier)."""
    plan = {s["n"]: s for s in p["plan"]}
    memo = {}

    def will_run(s, depth=0):
        if s["status"] != "todo":
            return False
        if s["host"] is None:
            return True
        if not p["counts_recovery"] or depth > 8:
            return False
        h = plan.get(s["host"])
        return h is not None and will_run(h, depth + 1)

    def inputs_ok(n, stack=()):
        if n in memo:
            return memo[n]
        s = plan.get(n)
        if s is None:
            raise ParseGap("h2_chain_step_unknown")
        if s["status"] == "done":
            memo[n] = True
            return True
        if n in stack:
            raise ParseGap("h2_chain_cycle")
        ok = True
        for r in s["refs"]:
            if r["level"] == 4 and r["kind"] == "chain":
                if not inputs_ok(r["step"], stack + (n,)):
                    ok = False
                continue
            f = resolve(r, s, facts, notes)
            if f is None:
                ok = False
                notes.append("unresolved")
            elif f["turn"] in redacted:
                ok = False
        memo[n] = ok
        return ok

    return {s["n"]: ("ok" if inputs_ok(s["n"]) else "fail") for s in p["plan"] if will_run(s)}


def solve(context):
    p = parse(context)
    allf = fact_table(p["events"])
    check_no_same_value_supersession(allf)
    q = quoted_fact(p, allf)
    ctxf = [f for f in allf if f["ftype"] != "M"]
    notes = []
    base = run_plan(p, ctxf, set(), notes)
    abl = run_plan(p, ctxf, {q["turn"]}, notes)
    broke = [n for n in sorted(base) if base[n] == "ok" and abl.get(n) == "fail"]
    p["notes"] = sorted(set(notes))
    p["broken_steps"] = broke
    return ("KEEP" if broke else "DROP"), p


def coverage(context):
    """Resolver coverage (K28 style): every reference of EVERY plan step (todo, done, contingency) against the context.
    -> (references, resolved, by_level) where by_level maps 'L1'.. to [references, resolved]."""
    p = parse(context)
    facts = [f for f in fact_table(p["events"]) if f["ftype"] != "M"]
    plan = {s["n"]: s for s in p["plan"]}
    tot = res = 0
    by = {}
    for s in p["plan"]:
        for r in s["refs"]:
            if r["level"] == 4 and r["kind"] == "chain":
                ok = r["step"] in plan
            else:
                ok = resolve(r, s, facts, []) is not None
            key = "L%d" % r["level"]
            by.setdefault(key, [0, 0])
            by[key][0] += 1
            by[key][1] += 1 if ok else 0
            tot += 1
            res += 1 if ok else 0
    return tot, res, by
