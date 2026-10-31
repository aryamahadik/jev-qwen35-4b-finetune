"""Hand-built RENDERED rows for the solver-B tests. Written from ROW_SCHEMA.md (the grammar) only: this is NOT the generator's renderer and uses
no generator code. Each builder returns a b-view dict {family, sub_block, options, rendered}."""

H1_OPTS = ["Delegate the subtask to a separate worker", "Carry out the subtask in the main thread"]
H2_OPTS = ["Keep this fact in the summary", "Drop this fact from the summary"]
H3_OPTS = ["Write out a plan before acting", "Act now without a plan"]
H1_Q = "Question: Should the agent hand this subtask to a separate worker, or do it itself in this thread?"
H2_Q = "Question: At the context summary, should this fact be kept in the summary or dropped?"
H3_Q = "Question: Before starting, does the agent need to plan the steps before acting, or just act now?"


def view(head, context, opts, question, order=(0, 1), sub_block=None):
    texts = [opts[i] for i in order]
    letters = "AB"
    options = [{"letter": letters[i], "label": "?", "text": t} for i, t in enumerate(texts)]
    otext = "\n".join("%s) %s" % (o["letter"], o["text"]) for o in options)
    return {"family": "T60", "sub_block": sub_block or head, "options": options,
            "rendered": {"context": context, "question": question, "options_text": otext, "text": context + "\n\n" + question + "\n" + otext}}


# ----------------------------------------------------------------------------------------------------------------------
# H1
# ----------------------------------------------------------------------------------------------------------------------
def h1_card(S, V, B, R):
    return ("Policy card zeta_alpha.\n"
            "Delegate a subtask only when all four conditions hold. First: it has at least %d steps, or it reads at least %d tokens.\n"
            "Second: the worker needs at most %d facts from the main thread.\n"
            "Third: its result is at most %d tokens long.\n"
            "Fourth: it shares no written resource with the main thread and needs no pending main step. Otherwise do it here." % (S, V, B, R))


def h1_context(S, V, B, R, nsteps, read_tokens, nneeds, result, shared=False, pending_feed=False, card=None, extra_pending=2):
    handles = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel"]
    facts = "\n".join("- the %s is %d" % (h, 10 + i) for i, h in enumerate(handles))
    pend = []
    for i in range(extra_pending):
        pend.append("- m%d: reads /work/p/in%d.cfg; writes /work/p/log%d.log" % (i + 1, i + 1, i + 1))
    out_path = "/work/p/out.dat"
    if shared:
        pend[0] = "- m1: reads /work/p/in1.cfg, %s; writes /work/p/log1.log" % out_path
    steps = "\n".join("  %d. check the item%d" % (i + 1, i + 1) for i in range(nsteps))
    files = []
    if read_tokens > 0:
        half = read_tokens // 2
        files = ["- reads /work/p/a.dat (%d tokens)" % half, "- reads /work/p/b.dat (%d tokens)" % (read_tokens - half)]
    needs = "nothing" if nneeds == 0 else ", ".join("the " + h for h in handles[:nneeds])
    incoming = "m2" if pending_feed else "none"
    ctx = [card or h1_card(S, V, B, R),
           "The main thread is busy with the widget rs. It holds the facts below and has pending steps.",
           "Main thread facts:", facts, "Main thread pending steps:", "\n".join(pend), "Candidate subtask (hand-off brief):", "- steps:", steps]
    ctx += files
    ctx += ["- returns a summary of the findings (%d tokens)" % result, "- needs from the main thread: %s" % needs, "- writes: %s" % out_path,
            "- input from pending main steps: %s" % incoming]
    return "\n".join(x for x in ctx if x != "")


def h1_view(*a, order=(0, 1), **kw):
    return view("h1", h1_context(*a, **kw), H1_OPTS, H1_Q, order)


# ----------------------------------------------------------------------------------------------------------------------
# H3
# ----------------------------------------------------------------------------------------------------------------------
def h3_card(H, n, unit="files"):
    return ("Policy card kappa_beta.\n"
            "Plan before acting only when all three conditions hold. First: some step is high stakes (it cannot be undone, reaches outside the team, "
            "or changes %d or more %s).\n"
            "Second: the task has at least %d steps.\n"
            "Third: the request does not say in what order the steps must run. Otherwise act." % (H, unit, n))


def step_line(sid, phrase, n, unit, effect):
    return "- %s: %s (changes %d %s; %s)" % (sid, phrase, n, unit, effect)


def h3_context(H, n_min, steps, order=(), flow=(), unit="files", order_style=0):
    """steps: [(phrase, N, effect)]; order, flow: [(a, b)] with 1-based step numbers (a before b)."""
    lines = [h3_card(H, n_min, unit), "The request: carry out the steps listed below.", "Order given in the request:"]
    if order:
        for a, b in order:
            lines.append(("- Do step s%d before step s%d." if (order_style + a) % 2 == 0 else "- Step s%d has to come before step s%d.") % (a, b))
    else:
        lines.append("- no order is given")
    lines.append("Steps:")
    for i, (phrase, n, eff) in enumerate(steps):
        lines.append(step_line("s%d" % (i + 1), phrase, n, unit, eff))
    lines.append("Data flow (a step that uses another step's output):")
    if flow:
        for a, b in flow:
            lines.append("- s%d uses the output of s%d" % (b, a))
    else:
        lines.append("- no step uses another step's output")
    return "\n".join(lines)


def h3_view(*a, opt_order=(0, 1), **kw):
    return view("h3", h3_context(*a, **kw), H3_OPTS, H3_Q, opt_order)


EFFECT_UNDOABLE = ["can be undone for 14 more days", "creates a new object that can be removed again"]
EFFECT_REPO_UNDOABLE = ["the working tree is clean, so git can restore it", "creates a new file in this session"]
EFFECT_HIGH = ["cannot be undone", "reaches people outside the team"]
EFFECT_REPO_HIGH = ["the file was made in this session and is not tracked"]


# ----------------------------------------------------------------------------------------------------------------------
# H2
# ----------------------------------------------------------------------------------------------------------------------
def card_h2(counts):
    rec = ("A step that runs only on failure (rollback, retry, read-back) counts as a step still to run." if counts else
           "A step that runs only on failure (rollback, retry, read-back) does not count as a step still to run.")
    return "Policy card sigma_pi.\nKeep a fact in the summary if a step still to run will take it from the conversation context.\n" + rec


def ref_l1(h):
    return "the %s" % h


def ref_l2(kind, entity):
    return {"V": "the value given for the %s", "R": "the value returned for the %s", "D": "the value we agreed for the %s",
            "S": "the key recorded for the %s", "P": "the saved location for the %s"}[kind] % entity


def ref_l3(ordinal):
    return "the %s record fetched by a get call" % ordinal


def ref_chain(k, sid_style=False):
    return "the value derived in step %s%d" % ("s" if sid_style else "", k)


def ref_ptr(entity):
    return "the saved location of the %s snapshot" % entity


def plan_line(n, status, verb, entity, refs, host=None):
    head = "[%s] step %d" % (status, n)
    if host:
        head += " (only if step %d fails)" % host
    return "%s: %s the %s%s" % (head, verb, entity, (" using " + " and ".join(refs)) if refs else "")


def ev(kind, *a):
    """kind: V(handle, entity, value, emph=None) | D(handle, entity, value, emph) | get(entity, handle, value) | create(entity, handle, value) |
    export(entity, path) | read(entity, source, handle, value) | check(entity) | M(handle, entity, value) -> list of lines (no turn number yet)."""
    if kind == "V":
        h, e, v = a[:3]
        em = (" (%s)" % a[3]) if len(a) > 3 and a[3] else ""
        return ["User: The %s for the %s is %s%s." % (h, e, v, em)]
    if kind == "D":
        h, e, v = a[:3]
        em = (" (%s)" % a[3]) if len(a) > 3 and a[3] else ""
        return ["User: Let us go with %s as the %s of the %s%s." % (v, h, e, em)]
    if kind == "M":
        h, e, v = a
        return ["User: As a reminder, the %s for the %s is %s." % (h, e, v)]
    if kind == "check":
        e = a[0]
        return ['Agent called check_%s(%s_id="%s-100")' % (e, e, e[:3]), "  -> output:", "     status: ok"]
    if kind in ("get", "create"):
        e, h, v = a[:3]
        em = (" (%s)" % a[3]) if len(a) > 3 and a[3] else ""
        call = ('get_%s(%s_id="%s-27")' % (e, e, e[:3])) if kind == "get" else ('create_%s(name="x-1")' % e)
        return ["Agent called " + call, "  -> output:", "     %s: %s%s" % (h, v, em)]
    if kind == "export":
        e, path = a
        return ['Agent called export_%s(target="%s")' % (e, e), "  -> output:", "     path: %s" % path]
    if kind == "read":
        e, src, h, v = a
        return ['Agent called read_%s(source="%s")' % (e, src), "  -> output:", "     %s: %s" % (h, v)]
    raise ValueError(kind)


TYPE_WORD = {"V": "a value given by the user", "R": "a tool result", "D": "a decision taken earlier", "S": "a state key", "P": "a saved location"}


def h2_context(counts, plan, events, quote_turn, quote_type, quote_handle, quote_value, task="Task: finish the work on the thing ab."):
    lines = [card_h2(counts), task, "Remaining plan:"]
    lines += plan
    lines.append("Context transcript:")
    for i, ev_lines in enumerate(events):
        for j, t in enumerate(ev_lines):
            lines.append(("(%d) " % (i + 1) if j == 0 else "    ") + t)
    lines.append("Fact in question (turn %d, %s): %s: %s" % (quote_turn, TYPE_WORD[quote_type], quote_handle, quote_value))
    return "\n".join(lines)


def h2_view(*a, opt_order=(0, 1), **kw):
    return view("h2", h2_context(*a, **kw), H2_OPTS, H2_Q, opt_order)
