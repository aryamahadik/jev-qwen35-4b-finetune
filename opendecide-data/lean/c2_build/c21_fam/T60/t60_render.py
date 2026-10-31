"""T60 rendering + finalisation: scene -> text (card, head block, question, options), line-level span map (kind per line, used by the pair /
quad integrity gates), option order with a balanced gold position, name-id collection, G10 decision spans. Labels come from SOLVER A only
(t60_rule). CODE ONLY.
"""
import hashlib
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from tool_engine import render, util, wording  # noqa: E402
import t60_ballast as ballast  # noqa: E402
import t60_levels as levels  # noqa: E402
import t60_model as M  # noqa: E402
import t60_rule as rule  # noqa: E402

EFFECT_UNDO = {"restore": "restore", "release": "release", "cancel": "cancel", "delete": "delete"}
TYPE_WORD = {"V": "a value given by the user", "R": "a tool result", "D": "a decision taken earlier", "S": "a state key", "P": "a saved location"}
ROLE_DESC = {"V": "the value given for the {entity}", "R": "the value returned for the {entity}", "D": "the value we agreed for the {entity}",
             "S": "the key recorded for the {entity}", "P": "the saved location for the {entity}"}
EMPH = ("a striking value", "a remarkable value", "a notable value")


def ln(kind, text):
    return dict(kind=kind, text=text)


def _fill(rec, tpl, slots, keep=()):
    used = wording.template_slots(tpl)
    out = wording.fill(tpl, slots)
    rec["slots"].update({k: slots[k] for k in used if k in keep})
    return out


def _pick(ctx, g, rec, form, key):
    f, i, tpl = ctx.pick(form, g["gid"], key)
    rec["wording_parts"].append((form, i))
    return tpl


def card_lines(ctx, g, rec, scene):
    card = scene["card"]
    head = scene["head"]
    title = ctx.names.card_title(card["id"])
    out = [ln("card_title", _fill(rec, _pick(ctx, g, rec, "clause.title", "title"), dict(title=title)))]
    pk = lambda f, k: _pick(ctx, g, rec, f, k)                 # noqa: E731
    if head == "h1":
        out.append(ln("card_size", _fill(rec, pk("clause.d_size", "size"), dict(s=card["S_min"], v=card["V"]), keep=("s", "v"))))
        out.append(ln("card_brief", _fill(rec, pk("clause.d_brief", "brief"), dict(b=card["B_max"]), keep=("b",))))
        out.append(ln("card_bound", _fill(rec, pk("clause.d_bound", "bound"), dict(r=card["R_max"]), keep=("r",))))
        out.append(ln("card_free", pk("clause.d_free", "free")))
    elif head == "h2":
        out.append(ln("card_keep", pk("clause.k_rule", "keep")))
        out.append(ln("card_recover", pk("clause.k_recover_on" if card["counts_recovery"] else "clause.k_recover_off", "recover")))
    else:
        out.append(ln("card_r1", _fill(rec, pk("clause.p_r1", "r1"), dict(h=card["H"], unit_pl=scene["ent"]["unit_pl"]), keep=("h",))))
        out.append(ln("card_r2", _fill(rec, pk("clause.p_r2", "r2"), dict(n=card["n_min"]), keep=("n",))))
        out.append(ln("card_r3", pk("clause.p_r3", "r3")))
    return out


# ======================================================================================================================
# H1
# ======================================================================================================================
def render_h1(ctx, g, rec, scene):
    ent = scene["ent"]
    b, main = scene["brief"], scene["main"]
    lines = []
    ref = ctx.names.other("category", g["gid"] + ":ref")
    lines.append(ln("h1_task", _fill(rec, _pick(ctx, g, rec, "task.h1", "task"), dict(entity=ent["nouns"][0], ref=ref))))
    lines.append(ln("h1_label", "Main thread facts:"))
    for f in main["facts"]:
        val = ("the %s plus %s" % (f["derived_from"], f["value"])) if f.get("derived_from") else f["value"]       # a DERIVABLE fact (coupling L4)
        lines.append(ln("h1_main", "- the %s is %s" % (f["handle"], val)))
        rec["slots"].setdefault("fv_" + f["handle"], f["value"])
    lines.append(ln("h1_label", "Main thread pending steps:"))
    for p in main["pending"]:
        lines.append(ln("h1_pending", "- %s: reads %s; writes %s" % (p["id"], ", ".join(p["reads"]), ", ".join(p["writes"]))))
    lines.append(ln("h1_label", "Candidate subtask (hand-off brief):"))
    lines.append(ln("h1_label", "- steps:"))
    for i, st in enumerate(b["steps"]):
        lines.append(ln("h1_step", "  %d. %s" % (i + 1, st)))
    for f in b["files"]:
        lines.append(ln("h1_file", "- reads %s (%d tokens)" % (f["path"], f["tokens"])))
    lines.append(ln("h1_result", "- returns a summary of the findings (%d tokens)" % b["result_tokens"]))
    lines.append(ln("h1_need", "- needs from the main thread: %s" % (", ".join("the " + h for h in b["needs"]) if b["needs"] else "nothing")))
    lines.append(ln("h1_write", "- writes: %s" % ", ".join(b["writes"])))
    lines.append(ln("h1_incoming", "- input from pending main steps: %s" % (", ".join(b["incoming"]) if b["incoming"] else "none")))
    return lines, dict(user=[], used_verbs=set(), used_roles=set(), used_progs=set(), outputs=[], carriers={"carrier.subtask_brief", "carrier.task_statement"})


# ======================================================================================================================
# H3
# ======================================================================================================================
def effect_phrase(scene, s):
    e = s["effect"]
    if scene["world"] == "repo":
        if e.get("backup"):
            return "the working tree is clean, so git can restore it"
        if e["kind"] == "create":
            return "creates a new file in this session"
        return "the file was made in this session and is not tracked"
    u = e.get("undo")
    window = (u.get("window", u.get("remaining", 0)) if u is not None else 0)
    delay = (u.get("delay", 0) if u is not None else 0)
    if e.get("external"):
        if u is not None and window >= 1:                                   # an undo path exists, the effect still reaches people outside the team
            return "reaches people outside the team (can be undone for %d more days)" % window
        return "reaches people outside the team"
    if e["kind"] == "create" and e.get("created_by_agent"):
        return "creates a new object that can be removed again"
    if u is not None and window >= 1:
        if delay >= 1:                                                      # the undo window runs from now, the step runs later
            return "can be undone for %d more days (the step runs in %d days)" % (window, delay)
        return "can be undone for %d more days" % window
    return "cannot be undone"


def step_phrase(scene, s):
    if scene["world"] == "repo":
        return "%s %s%s" % (s["verb"], s["target"], (" " + s["dest"]) if s.get("dest") else "")
    return "%s the %s %s" % (s["verb"], s["entity"], s["target"])


def render_h3(ctx, g, rec, scene):
    lines = []
    ent = scene["ent"]
    unit_pl = ent["unit_pl"]
    ids = [s["sid"] for s in scene["steps"]]
    tpl = _pick(ctx, g, rec, "task.h3_goal", "goal")
    lines.append(ln("h3_goal", _fill(rec, tpl, dict(verb_phrase="carry out the steps listed below"))))
    lines.append(ln("h3_label", "Order given in the request:"))
    if scene.get("order_form") == "numbered":                               # a numbered list states the order of the steps as listed (depvis L2)
        lines.append(ln("h3_order", "- the steps are numbered in the order in which they are to be carried out"))
    elif scene["stated_edges"]:
        for a, b in scene["stated_edges"]:
            lines.append(ln("h3_order", "- " + _fill(rec, _pick(ctx, g, rec, "order.line", "ord:%s>%s" % (a, b)), dict(a=a, b=b))))
    else:
        lines.append(ln("h3_order", "- no order is given"))
    lines.append(ln("h3_label", "Steps:"))
    for s in scene["steps"]:
        lines.append(ln("h3_step", "- %s: %s (changes %d %s; %s)" % (s["sid"], step_phrase(scene, s), s["effect"]["magnitude"], unit_pl,
                                                                      effect_phrase(scene, s))))
    lines.append(ln("h3_label", "Data flow (a step that uses another step's output):"))
    if scene["edges"]:
        derived = {tuple(e) for e in scene.get("derived_edges", [])}
        for a, b in scene["edges"]:
            if tuple((a, b)) in derived:                                    # the dependency runs through a derived value (depvis L4)
                lines.append(ln("h3_flow", "- %s uses a value derived from the output of %s" % (b, a)))
            else:
                lines.append(ln("h3_flow", "- %s uses the output of %s" % (b, a)))
    else:
        lines.append(ln("h3_flow", "- no step uses another step's output"))
    verbs = {s["verb"] for s in scene["steps"]}
    ex = dict(user=[ln("h3_goal", lines[0]["text"])] + [x for x in lines if x["kind"] == "h3_order"], used_verbs=set() if scene["world"] == "repo" else verbs,
              used_roles=set(), used_progs=verbs if scene["world"] == "repo" else set(), outputs=[],
              carriers={"carrier.task_statement", "carrier.user_turn"})
    return lines, ex


# ======================================================================================================================
# H2
# ======================================================================================================================
def ref_text(ref, scene):
    lv = ref["level"]
    if lv == 1:
        return "the %s" % ref["handle"]
    if lv == 2:
        return ROLE_DESC[ref["ftype"]].format(entity=ref["entity"])
    if lv == 3:
        return "the %s record fetched by a get call" % M_ORD[ref["ordinal"] - 1]
    if "via" in ref:
        return "the value derived in step %s" % ref["via"]
    ptr = next(f for f in scene["facts"] if f["type"] == "P" and f.get("art") == ref["pointer"])
    return "the saved location of the %s snapshot" % ptr["entity"]


M_ORD = ("first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth")      # up to 9 facts exist in a scene


def fact_sentence(scene, f, ctx, rng_key):
    """The transcript text of one fact: -> (lines of text, kind of event, call text)."""
    mk = set(f["markers"])
    emph = ""
    if "mark.t60.emphasis" in mk:
        emph = " (%s)" % EMPH[int(hashlib.sha256((scene["spec_id"] + f["id"]).encode()).hexdigest(), 16) % len(EMPH)]
    t = f["type"]
    ent = f["entity"]
    if t == "V":
        return ["User: The %s for the %s is %s%s." % (f["handle"], ent, f["value"], emph)], None
    if t == "D":
        return ["User: Let us go with %s as the %s of the %s%s." % (f["value"], f["handle"], ent, emph)], None
    if f.get("content_of"):
        ptr = rule.fact_by_id(scene, f["content_of"])
        call = 'read_%s(source="%s")' % (ent, ptr["value"])
        return ["Agent called %s" % call, "  -> output:", "     %s: %s%s" % (f["handle"], f["value"], emph)], call
    if t == "P":
        call = 'export_%s(target="%s")' % (ent, ent)
        return ["Agent called %s" % call, "  -> output:", "     path: %s%s" % (f["value"], emph)], call
    if t == "S":
        call = 'create_%s(name="%s")' % (ent, "x-" + f["id"][1:])
        return ["Agent called %s" % call, "  -> output:", "     %s: %s%s" % (f["handle"], f["value"], emph)], call
    call = 'get_%s(%s_id="%s-%s")' % (ent, ent, ent[:3], f["id"][1:] + "7")
    return ["Agent called %s" % call, "  -> output:", "     %s: %s%s" % (f["handle"], f["value"], emph)], call


def render_h2(ctx, g, rec, scene):
    lines = []
    rng = ctx.rng("r", g["gid"], "h2")
    ent0 = scene["ent"]["nouns"][0]
    quote = rule.fact_by_id(scene, scene["quote"])
    lines.append(ln("h2_task", _fill(rec, _pick(ctx, g, rec, "task.h2_task", "task"),
                                      dict(entity=ent0, ref=ctx.names.other("category", g["gid"] + ":ref")))))
    lines.append(ln("h2_label", "Remaining plan:"))
    steps_by = {s["sid"]: s for s in scene["plan"]}
    for k, s in enumerate(scene["plan"]):
        refs = " and ".join(ref_text(r, scene) for r in s["refs"])
        head = "[%s] step %s" % (s["status"], s["sid"][1:])
        if s.get("cond_host"):
            head += " (only if step %s fails)" % s["cond_host"][1:]
        verb = s["verb"]
        text = "%s: %s the %s" % (head, verb, s["entity"]) + ((" using " + refs) if refs else "")
        kind = "h2_planref" if s["sid"] == scene["star"] else "h2_plan"
        lines.append(ln(kind, text))
    lines.append(ln("h2_label", "Context transcript:"))
    # events: facts by idx, with 1-2 distractor events spliced in at fixed positions
    ev = []
    for f in sorted(scene["facts"], key=lambda x: x["idx"]):
        txt, call = fact_sentence(scene, f, ctx, f["id"])
        ev.append((f, txt))
    distract = rng.randint(1, 2)
    for j in range(distract):
        pos = rng.randint(0, len(ev))
        nm = scene["ent"]["nouns"][(j + 3) % 6]
        ev.insert(pos, (None, ["Agent called check_%s(%s_id=\"%s-%d\")" % (nm, nm, nm[:3], 100 + j), "  -> output:", "     status: ok"]))
    # skeptic fix: a `repeat` marker adds the fact's second turn at the END of the transcript, so it never renumbers the turns that follow
    # the fact and the four cells of a quad keep identical turn numbers (the distractor draws above do not depend on the marker either)
    for f in sorted(scene["facts"], key=lambda x: x["idx"]):
        if "mark.t60.repeat" in f["markers"] and f["type"] in ("V", "D"):
            ev.append((f, ["User: As a reminder, the %s for the %s is %s." % (f["handle"], f["entity"], f["value"])]))
    turn_of = {}
    outputs = []
    for k, (f, txt) in enumerate(ev):
        n = k + 1
        if f is not None and f["id"] not in turn_of and not txt[0].startswith("User: As a reminder"):
            turn_of[f["id"]] = n
        kind = "h2_fact" if (scene.get("h2kind") == "quad" and f is not None and f["id"] == scene["quote"]) else "h2_event"
        for j, t in enumerate(txt):
            lines.append(ln(kind, ("(%d) " % n if j == 0 else "    ") + t))
        if any(t.startswith("     ") for t in txt):
            outputs.append("\n".join(t.strip() for t in txt if t.startswith("     ")))
    where = "turn %d, %s" % (turn_of[quote["id"]], TYPE_WORD[quote["type"]])
    qtext = ("path: %s" % quote["value"]) if quote["type"] == "P" else ("%s: %s" % (quote["handle"], quote["value"]))
    lines.append(ln("h2_quote", _fill(rec, _pick(ctx, g, rec, "quote", "quote"), dict(where=where, text=qtext))))
    rec["slots"]["qvalue"] = quote["value"]
    verbs = set()
    for s in scene["plan"]:
        verbs.add(s["verb"])
    for f in scene["facts"]:
        verbs.add({"R": "get", "S": "create", "P": "export"}.get(f["type"], "get") if not f.get("content_of") else "read")
    verbs.add("check")
    user = [ln("h2_task", lines[0]["text"])] + [x for x in lines if x["kind"] in ("h2_event", "h2_fact") and x["text"].lstrip("()0123456789 ").startswith("User:")]
    return lines, dict(user=user, used_verbs=verbs, used_roles={"name", "target", "source"}, used_progs=set(), outputs=outputs,
                       carriers={"carrier.plan_block", "carrier.context_transcript", "carrier.fact_quote", "carrier.tool_output", "carrier.user_multi_turn",
                                 "carrier.call_history_list", "carrier.tool_output_prior", "carrier.task_statement"})


# ======================================================================================================================
# finalize
# ======================================================================================================================
OPT_LABELS = {"h1": rule.H1_LABELS, "h2": rule.H2_LABELS, "h3": rule.H3_LABELS}


def finalize(ctx, g, scene, pos, i_member):
    gid = g["gid"]
    head = scene["head"]
    rec = dict(family=M.FAMILY, slots={}, wording_parts=[])
    rec["pair_role"] = g.get("roles", [None, None, None, None])[i_member] if g["kind"] != "single" else None
    rec["row_id"] = "%s-%s" % (gid, rec["pair_role"] or ("s" if g["kind"] == "single" else str(i_member)))
    rec["group_id"] = gid
    gold = M.scene_gold(scene)
    rec["gold"] = gold
    lines = card_lines(ctx, g, rec, scene)
    if scene.get("ballast"):                                                 # the length mechanism: identical neutral notes on every member of a group
        lines.append(ln("note_label", ballast.LABEL))
        for t in scene["ballast"]:
            lines.append(ln("note", "  " + t))
    body, ex = {"h1": render_h1, "h2": render_h2, "h3": render_h3}[head](ctx, g, rec, scene)
    lines += body
    qform = "q." + head
    _f, qi, qtpl = ctx.pick(qform, gid, "q")
    rec["wording_parts"].append((qform, qi))
    texts = {}
    for lab in OPT_LABELS[head]:
        _f2, _i, tpl = ctx.pick("opt." + lab, gid, "opt:" + lab)
        texts[lab] = tpl
    order = util.place_gold(list(OPT_LABELS[head]), gold, int(pos), ctx.rng("pos", gid, i_member))
    opts = [dict(label=l, text=texts[l]) for l in order]
    letters = render.letter_options([o["text"] for o in opts])
    for o, (L, _t) in zip(opts, letters):
        o["letter"] = L
    rec["options"] = opts
    rec["gold_letter"] = next(o["letter"] for o in opts if o["label"] == gold)
    context = "\n".join(x["text"] for x in lines)
    question = "Question: " + qtpl
    otext = render.option_block(letters)
    rec["rendered"] = dict(context=context, question=question, options_text=otext, text=context + "\n\n" + question + "\n" + otext)
    rec["lines"] = [(x["kind"], x["text"]) for x in lines]
    user_txt = "\n".join(x["text"] for x in ex["user"])
    auth = authority_values(scene)
    rec["decision_spans"] = dict(field="parts.user", spans=render.decision_spans(user_txt, auth))
    rec["parts"] = dict(request=lines[len(lines) - len(body)]["text"] if body else "", card="\n".join(x["text"] for x in lines if x["kind"].startswith("card_")),
                        tools="", user=user_txt, outputs=ex["outputs"], conversation="\n".join(x["text"] for x in body), tail="")
    carriers = set(ex["carriers"])
    tool = sorted("verb." + v for v in ex["used_verbs"]) + sorted("param." + r for r in ex["used_roles"]) + sorted("prog." + p for p in ex["used_progs"])
    rec["names"] = {"policy": [scene["card"]["id"], "defs_card.t60." + {"h1": "delegate", "h2": "keep", "h3": "plan"}[head]], "tool": tool,
                    "language": [], "runner": [], "carrier": sorted(carriers)}
    rec["wording"] = dict(form_id="head.t60." + {"h1": "delegate", "h2": "keep", "h3": "plan"}[head],
                          idx=".".join("%s:%d" % (a, b) for a, b in rec["wording_parts"] if a.startswith(("q.", "task.", "clause."))))
    rec["template_id"] = "%s|%s|%s" % (head, scene["world"], g.get("kind"))
    rec["gold_pos"] = int(pos)
    rec.update(sub_block=head, block=g["block"], hd=head, hd_id=M.HEAD_IDS[head], world_kind=scene["world"], view=scene.get("view", "primary"),
               card=scene["card"]["id"], edit=scene.get("edit_ctx"), ctl=g.get("ctl"), lever_tag=scene.get("lever", "lever.none"), scene=scene,
               alarm=bool(scene.get("alarm")), levels=realised_levels(scene, rec), split=assign_split(g.get("scn", gid)), heldout_family=None,
               twin_of=None, row_level_target=None, cell=scene.get("cell"),
               h2kind=scene.get("h2kind"), call_text="",
               scenario_id=g.get("scn", gid),
               decisive=levels.decisive_mechanism(head, scene.get("edit_ctx"), g.get("ctl"), (g.get("rc") or {}).get("swap", {}).get("bind")))
    return rec


def assign_split(gid, dev_fraction=0.10):
    x = int(hashlib.sha256(("t60-split|" + gid).encode()).hexdigest()[:12], 16) / float(16 ** 12)
    return "dev" if x < dev_fraction else "train"


def authority_values(scene):
    """User-sourced content that limits the agent's procedure (G10 AUTHORITY, T60-B5): order statements and user-stated values."""
    out = []
    if scene["head"] == "h3":
        for a, b in scene["stated_edges"]:
            out.append("Do step %s before step %s" % (a, b))
            out.append("Step %s has to come before step %s" % (a, b))
    if scene["head"] == "h2":
        for f in scene["facts"]:
            if f["type"] in ("V", "D"):
                out.append(str(f["value"]))
    return out


def realised_levels(scene, rec):
    """Realised level of every mechanism and the row level (t60_levels; Opus ruling Q6)."""
    return levels.realised(scene, util.approx_tokens(rec["rendered"]["text"]))
