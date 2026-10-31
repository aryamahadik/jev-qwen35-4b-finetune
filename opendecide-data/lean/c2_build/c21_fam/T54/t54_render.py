"""T54 rendering + finalisation: structured record -> context/question/options text, option ordering with a balanced
gold position, name-id collection, wording bookkeeping. Labels come from SOLVER A only."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from tool_engine import render, state, util, wording  # noqa: E402
import t54_solver_a as sa  # noqa: E402
import t54_wording as tw  # noqa: E402

DECOY_FORMS = ("ticket ref {id}", "case no. {n}", "logged at {date}", "batch {n}", "lot {id}", 'tagged "{w}"')
STR_LIKE = ("str", "enum", "bool")


def _fill(rec, tpl, slots):
    """Fill a template and record exactly the slots it used (the slot round trip checks only those)."""
    used = wording.template_slots(tpl)
    out = wording.fill(tpl, slots)
    rec["slots"].update({k: slots[k] for k in used})
    return out


def decoy_phrase(rng, stem):
    f = rng.choice(DECOY_FORMS)
    return f.format(id="%s-%d" % (stem[:3], rng.randrange(100, 9999)), n=rng.randrange(10, 9000),
                    date="2026-%02d-%02d" % (rng.randrange(1, 13), rng.randrange(1, 29)),
                    w=rng.choice(["alpha", "bravo", "delta", "omega"]))


def decoy_clause(rng, stem, avoid=()):
    """An ambient clause with the SAME shape and vocabulary as an argument clause ('with <role> <value>'), using a role
    word the target tool does not have (`avoid`), so the request text alone cannot tell stated args from noise; whether
    the request supplies what the tool needs is read from the tool schema, which is the decision."""
    # never the generic `id` role: next to an entity's own `<entity>_id` parameter a 'with id <value>' clause reads as that
    # parameter's value, which would make an ASK row (the entity id unstated) arguable
    roles = [r for r in state.ROLES_T54 if r not in set(avoid) and r != "id"]
    r = rng.choice(roles)
    v = state.gen_value(rng, state.ROLE_TYPE[r], stem)
    return "with %s %s" % (pname_words(r), val_text(v, state.ROLE_TYPE[r]))


def build_clauses(rng, stem, args, n_decoys, skip=None, avoid=()):
    """', with <param> <value>' clauses for the stated args plus n_decoys ambient clauses, shuffled together."""
    items = ["with %s %s" % (pname_words(a["param"]), val_text(a["value"], a["type"]))
             for a in args if a["source"] == "user_turn" and a["param"] != skip]
    avoid = set(avoid) | {a["param"] for a in args}
    items += [decoy_clause(rng, stem, avoid) for _ in range(max(0, n_decoys))]
    rng.shuffle(items)
    return "".join(", " + it for it in items)


def val_text(v, ptype):
    """A value as written in a user turn: strings/enums quoted (one span), numbers/dates/ids bare (one span)."""
    if ptype in STR_LIKE and not any(ch.isdigit() for ch in str(v)):
        return '"%s"' % v
    return str(v)


def pname_words(p):
    return p.replace("_", " ")


def _tool(rec, tid):
    return next((t for t in rec["tools"] if t["tid"] == tid), None)


# =============================================================================================================
def _cards_text(ctx, g, rec, extra_notes):
    parts = []
    for cid in rec["cards"]:
        _f, idx, tpl = ctx.pick("card.%s" % cid, g["gid"], "card:" + cid)
        parts.append(tpl)
        rec["wording_parts"].append(("card." + cid, idx))
    parts.extend(extra_notes)
    return "\n".join(parts)


def _tools_text(rec):
    return "Tools:\n" + "\n".join("- " + render.render_tool_line(t) for t in rec["tools"])


def _turn_user(txt):
    return "User: " + txt


def _call_text(c, view, cap_tokens=256):
    s = "Agent called %s" % render.render_call(c["tool"], c["args"])
    if view == "view.with_outputs":
        if c.get("out") is None:
            s += "\n  -> (no output recorded)"
        else:
            o = render.kv_lines(c["out"])
            s += "\n  -> output:\n" + "\n".join("     " + ln for ln in o.splitlines())
    return s


def _clauses(args, skip=None):
    out = []
    for a in args:
        if a["source"] == "user_turn" and a["param"] != skip:
            out.append(", with %s %s" % (pname_words(a["param"]), val_text(a["value"], a["type"])))
    return "".join(out)


def _action(verb):
    a = tw.ACTION[verb]
    return a, a[:1].upper() + a[1:]


def _decoys(rng, stem, k):
    return [decoy_phrase(rng, stem) for _ in range(max(0, k))]


def _ambient(rng, stem, k):
    ds = _decoys(rng, stem, k)
    return ("Working notes: " + "; ".join(ds) + ".") if ds else ""


def render_s1(ctx, g, rec):
    """Every S1 row is an information request; pairD rows share the request text AND the two-span preface shape."""
    rng = ctx.rng("r", g["gid"], "s1")
    intent = rec["intent"]
    stem = intent.get("entity", "x")
    T = rec["span_total"]
    ent, field = intent["entity"], rec["flags"]["info_field"]
    ref = rec["flags"]["info_ref"]
    args = intent.get("args", [])
    ref_p = rec["flags"].get("ref_phrased")
    avoid = set(intent.get("target_params", []))
    n_user = len([a for a in args if a["source"] == "user_turn"])
    turns = []
    if intent["type"] == "info" or (rec["pair_role"] == "b" and rec["entry"] == "pairD"):
        # pairD: same request text in both rows; preface = the stated fact (ANSWER) or two ambient notes (CALL)
        req_rng = ctx.rng("r", g["gid"], "pairD-req")
        t_args = rec["flags"].get("text_args", [])
        clauses = build_clauses(req_rng, stem, t_args, T - 3 - len(t_args), avoid=avoid)
        _f, i2, t2 = ctx.pick("req.fetch", g["gid"], "fetch")
        req = _fill(rec, t2, dict(entity=ent, field=field, refpart=" " + ref, clauses=clauses))
        rec["wording_parts"].append(("req.fetch", i2))
        if intent["type"] == "info":
            f = rec["facts"][0]
            _f, i1, t1 = ctx.pick("fact.text", g["gid"], "fact")
            pre = _fill(rec, t1, dict(entity=f["entity"], field=f["field"], value=f["value"], ref=f["ref"]))
            rec["wording_parts"].append(("fact.text", i1))
        else:
            pre = "Working notes: %s; %s." % (decoy_phrase(rng, stem), decoy_phrase(rng, stem))
        return [], [_turn_user(pre), _turn_user(req)], None
    if ref_p:
        a_ref = next(a for a in args if a["param"] == ref_p)
        if a_ref["source"] == "user_turn":
            pre_ref = "Earlier I mentioned the %s %s." % (ent, ref)
        else:
            pre_ref = "Earlier I mentioned %s." % decoy_phrase(rng, stem)
        spans_used = (n_user - (1 if a_ref["source"] == "user_turn" else 0)) + 1
        _f, ir, tr_ = ctx.pick("req.fetch_ref", g["gid"], "fetchref")
        req = _fill(rec, tr_, dict(entity=ent, field=field,
                                   clauses=build_clauses(rng, stem, args, T - spans_used, skip=ref_p, avoid=avoid)))
        rec["wording_parts"].append(("req.fetch_ref", ir))
        return [], [_turn_user(pre_ref), _turn_user(req)], None
    # plain fetch: the ref is stated (CALL / NO_TOOL) or absent (ASK, default-declared pairC rows)
    stated_ref = ref if any(a["param"].endswith("_id") and a["source"] == "user_turn" for a in args) else None
    skip = next((a["param"] for a in args if a["param"].endswith("_id")), None)
    # every S1 row has exactly two user turns (preface + request) so the turn count is not a cue; a plain row's
    # preface is a two-span ambient note, like pairD's
    _f, ir, tr_ = ctx.pick("req.fetch", g["gid"], "fetch")
    clauses = build_clauses(rng, stem, args, T - n_user - 2, skip=skip, avoid=avoid)
    req = _fill(rec, tr_, dict(entity=ent, field=field, refpart=(" " + stated_ref) if stated_ref else "", clauses=clauses))
    rec["wording_parts"].append(("req.fetch", ir))
    pre = "Working notes: %s; %s." % (decoy_phrase(rng, stem), decoy_phrase(rng, stem))
    return [], [_turn_user(pre), _turn_user(req)], None


def render_s2(ctx, g, rec):
    rng = ctx.rng("r", g["gid"], rec["pair_role"] or "s")
    intent = rec["intent"]
    act, actc = _action(intent["verb"])
    _f, ir, tr_ = ctx.pick("req.act", g["gid"], "act" + (rec["pair_role"] or ""))
    n_user = len([a for a in intent["args"] if a["source"] == "user_turn"])
    slots = dict(action=act, action_cap=actc, entity=intent["entity"],
                 clauses=build_clauses(rng, intent["entity"], intent["args"], rec["span_total"] - n_user,
                                       avoid=intent.get("target_params", ())))
    req = _fill(rec, tr_, slots)
    rec["wording_parts"].append(("req.act", ir))
    return [], [_turn_user(req)], None


def _call_for_tool(t, vals, rng):
    """Argument SKELETON of a listed tool: its REQUIRED parameters as `name=<type>` placeholders (G0-lite S2: 'with its argument
    skeleton'). Never values: a value shown in an option would appear in the request only for the gold tool (a distractor's
    parameters are named differently), so a text-overlap heuristic picked the gold in 99.5% of rows (measured); with placeholders
    the decision stays what the G0-lite says, a match of verb, entity and parameter schema."""
    return "%s(%s)" % (t["name"], ", ".join("%s=<%s>" % (p["name"], p["type"]) for p in t["params"] if p["required"]))


def render_s3(ctx, g, rec):
    rng = ctx.rng("r", g["gid"], "s3")
    intent = rec["intent"]
    verb, ent = intent["verb"], intent["entity"]
    act, actc = _action(verb)
    c = rec["calls"][0]
    n_user = len([a for a in intent["args"] if a["source"] == "user_turn"])
    out_arg = next(a for a in intent["args"] if a["source"] in ("prior_tool_output", "missing_result"))
    _f, ir, tr_ = ctx.pick("req.act", g["gid"], "act")
    clauses = build_clauses(rng, ent, intent["args"], rec["span_total"] - n_user, avoid=intent.get("target_params", ()))
    slots = dict(action=act, action_cap=actc, entity=ent,
                 clauses=clauses + " (the %s from the earlier lookup)" % pname_words(out_arg["param"]))
    req = _fill(rec, tr_, slots)
    rec["wording_parts"].append(("req.act", ir))
    return [], [_turn_user("Session note: continuing earlier work."), ("CALL", c), _turn_user(req)], None


def render_s4(ctx, g, rec):
    intent, f = rec["intent"], rec["fact"]
    act, actc = _action(intent["verb"])
    rng = ctx.rng("r", g["gid"], "s4")
    n_user = len([a for a in intent["args"] if a["source"] == "user_turn"])
    _f, ir, tr_ = ctx.pick("req.act", g["gid"], "act")
    slots = dict(action=act, action_cap=actc, entity=intent["entity"],
                 clauses=build_clauses(rng, intent["entity"], intent["args"], rec["span_total"] - n_user,
                                       avoid=intent.get("target_params", ())))
    req = _fill(rec, tr_, slots)
    rec["wording_parts"].append(("req.act", ir))
    turns = [_turn_user("Session note: continuing earlier work.")]
    # decoy earlier read about another entity so 'an earlier call exists' is not a cue
    dt = _tool(rec, rec.get("decoy_read_tid")) if rec.get("decoy_read_tid") else None
    n_decoy = 2 - len(rec["calls"])                       # observed rows: 1 decoy + the fact read; others: 2 decoys
    if dt is not None and dt["params"]:
        for _ in range(n_decoy):
            pv = state.gen_value(rng, dt["params"][0]["type"], dt["entity"])
            turns.append(("CALL", dict(tool=dt["name"], args=[(dt["params"][0]["name"], pv)],
                                       out=[("state", rng.choice(["active", "closed", "pending"]))])))
    for c in rec["calls"]:
        turns.append(("CALL", c))
    turns.append(_turn_user(req))
    return [], turns, None


def render_s5(ctx, g, rec):
    # separate RNG streams per purpose, so a branch (a different edit) never shifts what another part draws
    r_amb, r_key, r_misc = ctx.rng("r", g["gid"], "s5-amb"), ctx.rng("r", g["gid"], "s5-key"), ctx.rng("r", g["gid"], "s5-misc")
    call = rec["call"]
    tool = _tool(rec, "t0")
    ent = tool["entity"]
    user_sents, outs = [], []
    other_keys = ["owner", "reference", "parent", "origin"]
    for i, a in enumerate(call["args"]):
        p, k = a["param"], a["prov"]
        c = a["ctx"]
        if c == "default":
            continue                                           # the only trace of the value is the schema default
        if c == "output_wrong":
            outs.append((other_keys[i % len(other_keys)], a["src_value"]))
        elif c == "output":
            outs.append((p, a["src_value"]))
        else:                                                  # user turn
            txt = a["src_value"] if k["kind"] == "transform" else val_text(a["src_value"], a["type"])
            user_sents.append("The %s uses %s %s." % (ent, pname_words(p), txt))
    conv_notes = []
    for conv in rec.get("declared_conversions", []):
        uf, ut, fac = ENTRY_UNITS[conv]
        conv_notes.append("Declared conversion: %s to %s, multiply by %d." % (uf, ut, fac))
    n_spans = sum(render.count_value_spans(s) for s in user_sents)
    ds = _ambient(r_amb, ent, max(0, rec["span_total"] - n_spans))
    turns = [_turn_user((" ".join(user_sents) + (" " + ds if ds else "")).strip() or "Working notes: none.")]
    rt = _tool(rec, "t0")
    # every S5 row has an earlier call whose output carries one decoy line under a role-like key, so neither the call nor
    # the key words (owner / reference / parent / origin) tell grounded from ungrounded
    free_keys = [k for k in other_keys if k not in {k2 for k2, _v in outs}]
    outs.append((r_key.choice(free_keys), state.gen_value(r_key, "str", ent)))
    r_misc.shuffle(outs)
    reader = next((t for t in rec["tools"] if t["tid"] != "t0" and t["rw"] == "read"), None)
    nm = reader["name"] if reader else "get_%s" % ent
    aname = (reader["params"][0]["name"] if reader and reader["params"] else "id")
    turns.append(("CALL", dict(tool=nm, args=[(aname, state.gen_value(r_misc, "str", ent))], out=outs)))
    act, actc = _action(rt["verb"])
    turns.append(_turn_user("Please %s the %s." % (act, ent)))
    prop = "Proposed call: " + render.render_call(call["name"], [(a["param"], a["value"]) for a in call["args"]])
    return conv_notes, turns, prop


ENTRY_UNITS = {"kg_to_g": ("kilograms", "grams", 1000), "km_to_m": ("kilometres", "metres", 1000),
               "min_to_s": ("minutes", "seconds", 60)}


def render_s6(ctx, g, rec):
    d = rec["dag"]
    tinfo = {t["id"]: t for t in d["node_tools"]}
    nodes_by_step = sorted(d["nodes"], key=lambda n: d["step_no"][n])
    lines_done, lines_todo = [], []
    for nid in nodes_by_step:
        args = []
        for a in d["args"][nid]:
            args.append("%s=%s" % (a["param"], ('<result of step %d>' % a["from_step"]) if a["from_step"] else '"%s"' % a["value"]))
        txt = "Step %d: %s(%s)" % (d["step_no"][nid], tinfo[nid]["tool"], ", ".join(args))
        if tinfo[nid]["alias"]:
            txt += " [also available as %s]" % tinfo[nid]["alias"]
        if nid in d["done"]:
            lines_done.append(txt + " -> done, result: %s" % d["results"][nid])
        else:
            lines_todo.append(txt)
    steps_text = "Steps still to run:\n" + "\n".join(lines_todo)
    if lines_done:
        steps_text = "Steps already done:\n" + "\n".join(lines_done) + "\n" + steps_text
    _f, ip, tp = ctx.pick("req.plan", g["gid"], "plan")
    req = "User: " + _fill(rec, tp, dict(steps="see the plan below"))
    rec["wording_parts"].append(("req.plan", ip))
    return [], [req], steps_text


RENDERERS = {"s1_need4": render_s1, "s2_pick": render_s2, "s3_limit": render_s3, "s4_precond": render_s4,
             "s5_argground": render_s5, "s6_parseq": render_s6}


def _turns_to_text(turns, view):
    out = []
    for t in turns:
        if isinstance(t, tuple):
            out.append(_call_text(t[1], view))
        else:
            out.append(t)
    return "\n".join(out)


def _options_for(ctx, g, rec, gold, pos):
    """Return option dicts in DISPLAY order with the gold at index `pos` (balanced across the sub-block)."""
    sb = rec["sub_block"]
    orng = ctx.rng("o", g["gid"], rec["pair_role"] or "s")
    if sb in ("s1_need4", "s3_limit", "s4_precond", "s5_argground"):
        labels = {"s1_need4": sa.S1_LABELS, "s3_limit": sa.S3_LABELS, "s4_precond": sa.S4_LABELS,
                  "s5_argground": sa.S5_LABELS}[sb]
        k = len(labels)
        order = util.place_gold(list(labels), gold, pos % k, orng)
        opts = []
        for l in order:
            _f, idx, tpl = ctx.pick("opt.%s" % l, g["gid"], "opt:" + l)
            opts.append(dict(label=l, text=tpl, wi=idx))
        return opts
    if sb == "s2_pick":
        by_tid = {t["tid"]: t for t in rec["tools"]}
        vals = {a["param"]: val_text(a["value"], a["type"]).strip('"') for a in rec["intent"]["args"]}
        tids = list(rec["shortlist_tids"])
        gold_tid = rec["intent"]["target_tid"]
        order = util.place_gold(tids, gold_tid, pos % 4, orng)
        return [dict(label=by_tid[t]["name"], text=_call_for_tool(by_tid[t], vals, ctx.rng("ov", g["gid"], t)), wi=0) for t in order]
    if sb == "s6_parseq":
        d = rec["dag"]
        opts = rec["s6_options"]
        gold_o = next(o for o in opts if o["label"] == gold)
        order = util.place_gold([o["label"] for o in opts], gold, pos % 4, orng)
        by_label = {o["label"]: o for o in opts}
        out = []
        for l in order:
            o = by_label[l]
            calls = []
            for nm, nid in o["parts"]:
                if nid == "x":
                    calls.append(render.render_call(nm, rec["extra_ready_args"]))
                else:
                    a = d["args"][nid]
                    calls.append("%s(%s)" % (nm, ", ".join('%s=%s' % (x["param"], ('<result of step %d>' % x["from_step"]) if x["from_step"] else '"%s"' % x["value"]) for x in a)))
            out.append(dict(label=l, text=" and ".join(calls), wi=0, canon=o["canon"]))
        return out
    raise ValueError(sb)


def collect_names(rec):
    verbs = sorted({"verb." + t["verb"] for t in rec["tools"]})
    params = sorted({p["role"] for t in rec["tools"] for p in t["params"] if p["role"]})
    carriers = set()
    sb = rec["sub_block"]
    carriers.add("carrier.user_single" if sb in ("s2_pick", "s6_parseq") else "carrier.user_multi_turn")
    if rec["view"] == "view.with_outputs":
        carriers.add("carrier.tool_output_prior")
    for c in rec.get("names_extra_carriers", []):
        carriers.add(c)
    return dict(policy=sorted(rec["cards"]), tool=verbs + params, language=[], runner=[], carrier=sorted(carriers))


def finalize(ctx, g, rec, pos):
    """Compute gold with solver A, order options, render, and attach bookkeeping. Returns the finished record."""
    sb = rec["sub_block"]
    rec["wording_parts"] = []
    rec["slots"] = {}
    rec["row_id"] = "%s-%s" % (g["gid"], rec["pair_role"] or "s")
    if sb == "s6_parseq":
        rec["options"] = [dict(label=o["label"], canon=o["canon"]) for o in rec["s6_options"]]
    gold = sa.gold_label(rec)
    rec["gold"] = gold
    notes, turns, tail = RENDERERS[sb](ctx, g, rec)
    opts = _options_for(ctx, g, rec, gold, pos)
    q_form = "q.%s" % sb
    _f, qi, qtpl = ctx.pick(q_form, g["gid"], "q")
    rec["wording_parts"].append((q_form, qi))
    card_text = _cards_text(ctx, g, rec, notes)
    ctx_parts = [card_text, _tools_text(rec), "Conversation:\n" + _turns_to_text(turns, rec["view"])]
    if tail:
        ctx_parts.append(tail)
    context = "\n\n".join(ctx_parts)
    letters = render.letter_options([o["text"] for o in opts])
    for o, (L, _t) in zip(opts, letters):
        o["letter"] = L
    rec["options"] = opts
    rec["gold_letter"] = next(o["letter"] for o in opts if o["label"] == gold)
    question = "Question: " + qtpl
    otext = render.option_block(letters)
    rec["rendered"] = dict(context=context, question=question, options_text=otext,
                           text=context + "\n\n" + question + "\n" + otext)
    rec["names"] = collect_names(rec)
    form = "%s|%s|%s" % (sb, rec["card"], rec["view"])
    # wording identity = the pool picks of the QUESTION, REQUEST and CARD forms only (a fact sentence or an ambient note
    # is content, not a wording-pool pick, and must not leak the label through this id)
    rec["wording"] = dict(form_id=form, idx=".".join("%s:%d" % (a, b) for a, b in rec["wording_parts"]
                                                      if a.startswith(("q.", "req.", "card."))))
    rec["template_id"] = "%s|%s|%s" % (rec["archetype"], rec["intent"].get("verb") or "-", rec["view"])
    rec["gold_pos"] = pos
    rec["call_bearing"] = sa.is_call_bearing(gold)
    # the user turns' real value-span count (regex over the rendered user text), for the P-6 gate
    user_txt = "\n".join(t for t in turns if isinstance(t, str))
    rec["user_spans"] = render.count_value_spans(user_txt)
    rec["view_tag"] = rec["view"]
    outs = []
    if rec["view"] == "view.with_outputs":
        outs = [render.kv_lines(t[1]["out"]) for t in turns if isinstance(t, tuple) and t[1].get("out")]
    last_user = next((t for t in reversed(turns) if isinstance(t, str)), "")
    auth = [a["value"] for a in rec["intent"].get("args", []) if a.get("source") == "user_turn" and a.get("value")]
    if rec["sub_block"] == "s5_argground":
        auth = [a["src_value"] for a in rec["call"]["args"] if a.get("ctx") == "user"]
    if rec["flags"].get("info_ref"):
        auth.append(rec["flags"]["info_ref"])
    rec["decision_spans"] = dict(field="parts.user", spans=render.decision_spans(user_txt, auth))
    rec["parts"] = dict(request=last_user, card=card_text, tools=_tools_text(rec), user=user_txt, outputs=outs, tail=tail or "",
                        conversation=_turns_to_text(turns, rec["view"]))
    return rec
