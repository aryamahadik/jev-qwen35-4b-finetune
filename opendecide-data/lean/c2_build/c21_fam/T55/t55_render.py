"""T55 rendering + finalisation (structured record -> text; labels from solver A only)."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from tool_engine import render, state, util, wording  # noqa: E402
import t55_solver_a as sa  # noqa: E402
import t55_wording as tw  # noqa: E402

TIMEOUT_PHRASES = ["no acknowledgement received", "connection closed before a reply"]


def _fill(rec, tpl, slots):
    used = wording.template_slots(tpl)
    out = wording.fill(tpl, slots)
    rec["slots"].update({k: slots[k] for k in used})
    return out


def pname_words(p):
    return p.replace("_", " ")


def _tool(rec, tid):
    return next((t for t in rec["tools"] if t["tid"] == tid), None)


def _words(v):
    return "ask the user" if v == "ASK" else "stop"


def card_text(ctx, g, rec):
    parts = []
    for cid in rec["cards"]:
        _f, idx, tpl = ctx.pick("card.%s" % cid, g["gid"], "card:" + cid)
        rec["wording_parts"].append(("card." + cid, idx))
        slots = {}
        if cid.startswith("card.t55.escalate_table"):
            slots = dict(quota=_words(rec["escalation"]["quota_exhausted"]), unsupp=_words(rec["escalation"]["unsupported_op"]))
        elif cid == "card.t55.denial_consec_total":
            c = rec["card_b5"]
            slots = dict(kc=c["K_c"], kt=c["K_t"])
        elif cid == "card.t55.denial_window":
            c = rec["card_b5"]
            slots = dict(kc=c["K_c"], kw=c["K_w"], w=c["W"])
        parts.append(_fill(rec, tpl, slots) if slots else tpl)
    if rec["sub_block"] == "b6_loop_poll":
        c = rec["card_b6"]
        _f, idx, tpl = ctx.pick("card.b6", g["gid"], "b6")
        rec["wording_parts"].append(("card.b6", idx))
        trans = ", ".join("%s->%s" % (a, b) for a, b in c["transitions"])
        parts.append(_fill(rec, tpl, dict(pcap=c["P_cap"], lim=c["L"], trans=trans, nw="cannot" if c["non_waitable"] else "can")))
    return "\n".join(parts)


def tools_text(rec):
    return "Tools:\n" + "\n".join("- " + render.render_tool_line(t) for t in rec["tools"])


def error_lines(rec, err):
    grp = err["group"]
    ch = err["channels"]
    lines = [("status", tw.STATUS_TOKEN[grp] if "hint" in ch else "error")]
    if "code" in ch:
        lines.append(("code", err["code"]))
    if "phrase" in ch:
        lines.append(("detail", tw.PHRASES[grp][err["phrase_idx"]]))
    if err["class"] == "rate_limited":
        lines.append(("retry_after", err["retry_after"]))
    if err.get("field"):
        lines.append(("field", err["field"]))
    return lines


def call_block(name, args, out_lines, extra_note=None):
    s = "Agent called %s" % render.render_call(name, args)
    if out_lines is not None:
        s += "\n  -> output:\n" + "\n".join("     " + ln for ln in render.kv_lines(out_lines).splitlines())
    return s


def _request(ctx, g, rec, rng):
    t0 = _tool(rec, rec["call"]["tool_tid"])
    ent = t0["entity"]
    if rec["sub_block"] == "b5_deny_escalate":
        _f, i, tpl = ctx.pick("req.denied", g["gid"], "req")
        rec["wording_parts"].append(("req.denied", i))
        return "User: " + _fill(rec, tpl, dict(entity=ent))
    if rec["sub_block"] == "b6_loop_poll":
        _f, i, tpl = ctx.pick("req.poll", g["gid"], "req")
        rec["wording_parts"].append(("req.poll", i))
        ref = rec["call"]["args"][0][1] if rec["call"]["args"] else "x"
        return "User: " + _fill(rec, tpl, dict(entity=ent, ref=ref))
    _f, i, tpl = ctx.pick("req.act", g["gid"], "req")
    rec["wording_parts"].append(("req.act", i))
    allv = list(rec["user_values"]) + list(rec.get("decoy_clauses", []))
    clauses = "".join(", with %s %s" % (pname_words(k), v) for k, v in allv)
    act = tw.ACTION[t0["verb"]]
    return "User: " + _fill(rec, tpl, dict(action=act, entity=ent, clauses=clauses))


def render_b1(ctx, g, rec, rng):
    t0 = _tool(rec, rec["call"]["tool_tid"])
    err = rec["error"]
    out = error_lines(rec, err)
    # the attempt counter is a state line, not a repeated block, so the row length does not depend on the attempt index
    blocks = [call_block(rec["call"]["name"], rec["call"]["args"], out), "Attempts of this call so far (including this one): %d." % rec["attempt"]]
    outs = [render.kv_lines(out)]
    return [_request(ctx, g, rec, rng)] + blocks, outs, None


def render_b2(ctx, g, rec, rng):
    ph = TIMEOUT_PHRASES[rng.randrange(len(TIMEOUT_PHRASES))]
    out = [("status", "timeout"), ("detail", ph)]
    blocks = [call_block(rec["call"]["name"], rec["call"]["args"], out)]
    outs = [render.kv_lines(out)]
    if rec["step"] == 1 and rec.get("decoy_read_tid"):          # keep step-1 rows as long as step-2 rows (no length cue)
        dt = _tool(rec, rec["decoy_read_tid"])
        do = [("status", "ok"), ("count", rng.randint(1, 9))]
        blocks.insert(0, call_block(dt["name"], [(p["name"], state.gen_value(rng, p["type"], dt["entity"]))
                                                 for p in dt["params"] if p["required"]], do))
        outs.insert(0, render.kv_lines(do))
    if rec["step"] == 2:
        tr = _tool(rec, "tr")
        a0 = rec["call"]["args"][0]
        ro = [("committed", "yes" if rec["readback"]["committed"] else "no")]
        blocks.append(call_block(tr["name"], [(tr["params"][0]["name"], a0[1])] if tr["params"] else [], ro))
        outs.append(render.kv_lines(ro))
    return [_request(ctx, g, rec, rng)] + blocks, outs, None


def result_lines(rec):
    r, c, b = rec["result"], rec["ctx"], rec["b3"]
    lines = [("status", "ok")]
    f = b["field"]
    if r.get("items") is not None:
        lines.append(("count", len(r["items"])))
        lines.append(("items", ", ".join(str(x) for x in r["items"]) if r["items"] else "(none)"))
    for k, v in r.get("fields", {}).items():
        lines.append((k, v))
    if r.get("total") is not None:
        lines.append(("total", r["total"]))
    if r.get("echo") is not None:
        lines.append(("detail", " ".join("%s=%s" % (k, v) for k, v in r["echo"].items())))
    return lines


def render_b3(ctx, g, rec, rng):
    r, c, b = rec["result"], rec["ctx"], rec["b3"]
    vt = b["vtype"]
    lines = []
    outs = []
    ctool = next((t for t in rec["tools"] if t["tid"] == "tc"), None) or \
        next((t for t in rec["tools"] if t["rw"] == "read" and t["tid"] != "t0"), None)
    cname = ctool["name"] if ctool else rec["call"]["name"]
    turns = [_request(ctx, g, rec, rng)]
    if vt == "empty_when_count_stated" and c.get("stated_count") is not None:
        o = [("count", c["stated_count"])]
        turns.append(call_block(cname, [], o))
        outs.append(render.kv_lines(o))
    if vt == "id_not_in_prior_list":
        o = [("count", len(c["prior_ids"])), ("items", ", ".join(c["prior_ids"]))]
        turns.append(call_block(cname, [], o))
        outs.append(render.kv_lines(o))
    if vt == "scale_mismatch":
        o = [(c["reference"]["field"], c["reference"]["value"])]
        turns.append(call_block(cname, [], o))
        outs.append(render.kv_lines(o))
    if vt == "stale_echo":
        turns[0] += ", and I want " + " and ".join("%s %s" % (k, v) for k, v in c["intended_args"].items())
        o = [("detail", " ".join("%s=%s" % (k, v) for k, v in c["prior_args"].items()))]
        turns.append(call_block(cname, [], o))
        outs.append(render.kv_lines(o))
    res = result_lines(rec)
    turns.append(call_block(rec["call"]["name"], rec["call"]["args"], res))
    turns.append("Attempts of this call so far (including this one): %d." % rec["attempt"])
    outs.append(render.kv_lines(res))
    return turns, outs, None


def render_b5(ctx, g, rec, rng):
    d, c = rec["denials"], rec["card_b5"]
    turns = [_request(ctx, g, rec, rng), call_block(rec["call"]["name"], rec["call"]["args"], None)]
    st = "Denials: %d consecutive, %d in total" % (d["n_c"], d["n_t"])
    if c["window"]:
        st += ", %d among the last %d calls" % (d["n_w"], c["W"])
    st += ".\nThe last call above was denied.\nAn alternative permitted path exists: %s.\nA fixed rule blocks the goal itself: %s." % (
        "yes" if d["alt_exists"] else "no", "yes" if d["goal_blocked_hard"] else "no")
    return turns, [], st


def render_b6(ctx, g, rec, rng):
    p = rec["poll"]
    turns = [_request(ctx, g, rec, rng)]
    outs = []
    for i, (args, ob) in enumerate(zip(p["calls"], p["obs"])):
        lines = []
        for k in ("progress", "status", "counter"):
            if k in ob:
                lines.append(("count" if k == "counter" else k, ob[k]))
        turns.append(call_block(rec["call"]["name"], args, lines))
        outs.append(render.kv_lines(lines))
    st = "Calls used on this poll: %d.\nAn alternative approach is available: %s." % (p["calls_used"], "yes" if p["alt_exists"] else "no")
    return turns, outs, st


RENDERERS = {"b1_classic": render_b1, "b4_blind_retry": render_b1, "b2_ambig_write": render_b2, "b3_implicit": render_b3,
             "b5_deny_escalate": render_b5, "b6_loop_poll": render_b6}


def collect_names(rec):
    verbs = sorted({"verb." + t["verb"] for t in rec["tools"]})
    params = sorted({p["role"] for t in rec["tools"] for p in t["params"] if p["role"]})
    sb = rec["sub_block"]
    car = {"b1_classic": ["carrier.tool_output_error"], "b4_blind_retry": ["carrier.tool_output_error"],
           "b2_ambig_write": ["carrier.tool_output_timeout"], "b3_implicit": ["carrier.tool_output_odd_success"],
           "b5_deny_escalate": ["carrier.state_block_counters"],
           "b6_loop_poll": ["carrier.state_block_counters", "carrier.call_history_list"]}[sb]
    if sb in ("b1_classic", "b4_blind_retry") and rec["attempt"] > 1:
        car = car + ["carrier.call_history_list"]            # the attempt counter line
    return dict(policy=sorted(rec["cards"]), tool=verbs + params, language=[], runner=[], carrier=sorted(set(car)))


def finalize(ctx, g, rec, pos):
    sb = rec["sub_block"]
    rec["wording_parts"] = []
    rec["slots"] = {}
    rec["row_id"] = "%s-%s" % (g["gid"], rec["pair_role"] or "s")
    gold = sa.gold_label(rec)
    rec["gold"] = gold
    rng = ctx.rng("r", g["gid"], rec["pair_role"] or "s")
    turns, outs, tail = RENDERERS[sb](ctx, g, rec, rng)
    labels = {"b1_classic": sa.B1_LABELS, "b4_blind_retry": sa.B1_LABELS, "b2_ambig_write": sa.B2_LABELS,
              "b3_implicit": sa.B3_LABELS, "b5_deny_escalate": sa.B5_LABELS, "b6_loop_poll": sa.B6_LABELS}[sb]
    orng = ctx.rng("o", g["gid"], rec["pair_role"] or "s")
    order = util.place_gold(list(labels), gold, pos % len(labels), orng)
    opts = []
    for l in order:
        _f, idx, tpl = ctx.pick("opt.%s" % l, g["gid"], "opt:" + l)
        opts.append(dict(label=l, text=tpl, wi=idx))
    q_form = "q.%s" % sb
    _f, qi, qtpl = ctx.pick(q_form, g["gid"], "q")
    rec["wording_parts"].append((q_form, qi))
    ctext = card_text(ctx, g, rec)
    conv = "\n".join(turns)
    parts = [ctext, tools_text(rec), "Conversation:\n" + conv]
    if tail:
        parts.append(tail)
    context = "\n\n".join(parts)
    letters = render.letter_options([o["text"] for o in opts])
    for o, (L, _t) in zip(opts, letters):
        o["letter"] = L
    rec["options"] = opts
    rec["gold_letter"] = next(o["letter"] for o in opts if o["label"] == gold)
    question = "Question: " + qtpl
    otext = render.option_block(letters)
    rec["rendered"] = dict(context=context, question=question, options_text=otext, text=context + "\n\n" + question + "\n" + otext)
    rec["names"] = collect_names(rec)
    rec["wording"] = dict(form_id="%s|%s|%s" % (sb, rec["cards"][0], rec["view"]),
                          idx=".".join("%s:%d" % (a, b) for a, b in rec["wording_parts"] if a.startswith(("q.", "req.", "card."))))
    t0 = _tool(rec, rec["call"]["tool_tid"])
    nb = 0 if len(rec["tools"]) <= 5 else (1 if len(rec["tools"]) <= 8 else 2)
    rec["template_id"] = "%s|%s|n%d|%s" % (rec["archetype"], t0["verb"], nb, sb)
    rec["gold_pos"] = pos
    rec["parts"] = dict(card=ctext, tools=tools_text(rec), request=turns[0], outputs=outs, tail=tail or "", conversation=conv)
    from tool_engine import perturb
    rec["cell"] = perturb.t55_cell(rec)
    rec["decision_spans"] = dict(field="parts.request", spans=render.decision_spans(turns[0], [v for _k, v in rec.get("user_values", [])]))
    return rec
