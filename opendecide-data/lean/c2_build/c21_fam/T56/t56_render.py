"""T56 rendering + finalisation (structured scenario -> text; labels from solver A only)."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from tool_engine import perturb, render, util, wording  # noqa: E402
import t56_solver_a as sa  # noqa: E402
import t56_wording as tw  # noqa: E402

# The card must not be a cue for the fault family either: every sub-block draws from the same cards; the D4 question form
# (ready to commit) always carries the commit policy, whose text states every condition the other cards state.
CARD_BY_SB = {sb: ("card.t56.evidence_required", "card.t56.fresh_run_required", "card.t56.entrypoint_reach")
              for sb in ("d1_evidence", "d2_ledger", "d3_demo_only", "d5_unverified")}
CARD_BY_SB["d4_ready"] = ("card.t56.scope_declared",)


def _fill(rec, tpl, slots):
    used = wording.template_slots(tpl)
    out = wording.fill(tpl, slots)
    rec["slots"].update({k: slots[k] for k in used})
    return out


def crit_text(ctx, g, rec, sc, c, idx):
    pred = c["pred"]
    _f, i, tpl = ctx.pick("crit.%s" % pred, g["gid"], "crit%d" % idx)
    rec["wording_parts"].append(("crit." + pred, i))
    slots = dict(item=c["item"], value=c["value"], field=sc["fv"], entity=sc["ent"])
    if pred == "reachable":
        slots = dict(item=sc["entry"], value=c["item"])
    return _fill(rec, tpl, slots) + (" (optional)" if c["optional"] else "")


def task_text(ctx, g, rec, sc):
    _f, i, tpl = ctx.pick("task.all", g["gid"], "task")
    rec["wording_parts"].append(("task.all", i))
    crit = "; ".join("%d) %s" % (n + 1, crit_text(ctx, g, rec, sc, c, n)) for n, c in enumerate(sc["criteria"]))
    return _fill(rec, tpl, dict(entity=sc["ent"], criteria=crit, scope=sc["scope"]))


def claim_text(ctx, g, rec, sc):
    pool = ctx.pool.pools.get("claim.all") or tw.CLAIMS["all"]            # the pool in use (the expanded one in production)
    k = g["claim_idx"] % len(pool)
    rec["wording_parts"].append(("claim.all", k))
    return _fill(rec, pool[k], dict(entity=sc["ent"]))


def call_text(c):
    s = "Agent called %s" % render.render_call(c["tool"], c["args"])
    s += "\n  -> output:\n" + "\n".join("     " + ln for ln in render.kv_lines(c["out"]).splitlines())
    return s


def collect_names(rec, sc):
    verbs = sorted({"verb." + c["tool"].split("_", 1)[0] for c in sc["calls"]})
    car = {"carrier.task_statement", "carrier.closing_claim"}
    fmt = set()
    for c in sc["calls"]:
        if c["kind"] == "check":
            car.add("carrier.tool_output_check")
            fmt.add("fmt.per_item_lines")
            if rec["style"] == "counts" and c.get("part") != "module":
                fmt.add("fmt.summary_counts")
        elif c["kind"] == "ledger":
            car.add("carrier.tool_output_ledger")
            fmt.add("fmt.ledger_rows")
        elif c["kind"] == "tree":
            car.add("carrier.tool_output_tree")
            fmt.add("fmt.tree_status")
        elif c["kind"] == "graph":
            fmt.add("fmt.module_graph")
    lang, runner = [sc["lang"]], [sc["runner"]]
    return dict(policy=[rec["card"]], tool=verbs, language=lang, runner=runner, carrier=sorted(car | fmt))


def _opt_labels(sb):
    return ("READY", "NOT_READY") if sb == "d4_ready" else ("DONE", "CONTINUE")


def finalize(ctx, g, sc, role, pos, fault):
    sb = g["sub_block"]
    gid = g["gid"]
    rec = dict(family="T56", sub_block=sb, entry=g["entry"], group_id=gid, pair_role=role, fault=fault, stage=g["stage"],
               view="view.with_outputs", hidden=sc["hidden"], calls=sc["calls"], criteria=sc["criteria"], style=g["style"],
               lang=sc.get("lang"), wording_parts=[], slots={}, row_id="%s-%s" % (gid, role or "s"))
    cards = CARD_BY_SB[sb]
    rec["card"] = cards[int(util.sha256_text("card|" + gid)[:4], 16) % len(cards)]
    rec["cards"] = [rec["card"]]
    label, reason = sa.gold(rec)
    rec["gold"], rec["gold_reason"] = label, reason
    rec["task_text"] = task_text(ctx, g, rec, sc)
    rec["claim"] = claim_text(ctx, g, rec, sc)
    rec["skeleton"] = [(c["tool"], [list(a) for a in c["args"]]) for c in sc["calls"] if c["kind"] != "check" or fault != "f_no_check"]
    q_form = "q.ready" if sb == "d4_ready" else "q.done"
    _f, qi, qtpl = ctx.pick(q_form, gid, "q")
    rec["wording_parts"].append((q_form, qi))
    labels = _opt_labels(sb)
    order = util.place_gold(list(labels), label, pos % 2, ctx.rng("o", gid, role or "s"))
    opts = []
    for l in order:
        _f, idx, tpl = ctx.pick("opt.%s" % l, gid, "opt:" + l)
        opts.append(dict(label=l, text=tpl, wi=idx))
    letters = render.letter_options([o["text"] for o in opts])
    for o, (L, _t) in zip(opts, letters):
        o["letter"] = L
    rec["options"] = opts
    rec["gold_letter"] = next(o["letter"] for o in opts if o["label"] == label)
    conv = "\n".join(call_text(c) for c in sc["calls"] if not (c["kind"] == "check" and fault == "f_no_check"))
    ctext = tw.CARDS[rec["card"]]
    context = "\n\n".join([ctext, "Task statement:\n" + rec["task_text"], "Trajectory:\n" + conv,
                           "Agent's closing message: \"%s\"" % rec["claim"]])
    question = "Question: " + qtpl
    otext = render.option_block(letters)
    rec["rendered"] = dict(context=context, question=question, options_text=otext, text=context + "\n\n" + question + "\n" + otext)
    rec["names"] = collect_names(rec, sc)
    rec["wording"] = dict(form_id="%s|%s|%s" % (sb, rec["card"], rec["view"]),
                          idx=".".join("%s:%d" % (a, b) for a, b in rec["wording_parts"] if a.startswith(("q.", "task.", "claim.", "crit."))))
    rec["claim_wording"] = rec["claim"]
    sig = ">".join(c["pred"][:3] + ("?" if c["optional"] else "") for c in sc["criteria"] if c["part"] == "store")
    rec["template_id"] = "%s|%s|%s|%d|%s" % (g["style"], sc["lang"], len(sc["recips"]), sc["n_store"], sig)
    rec["gold_pos"] = pos
    rec["bin"] = "hard" if fault in perturb.HARD_FAULTS else ("easy" if fault in perturb.EASY_FAULTS else "none")
    outs = [render.kv_lines(c["out"]) for c in sc["calls"] if not (c["kind"] == "check" and fault == "f_no_check")]
    rec["parts"] = dict(request=rec["task_text"], claim=rec["claim"], card=ctext, outputs=outs, conversation=conv, tail="",
                        task=rec["task_text"])
    rec["n_required"] = sc["n_req"]
    rec["head_selected"] = bool(g.get("head"))
    auth = [sc["scope"]] + [c["item"] for c in sc["criteria"] if c["pred"] != "reachable"] + \
        [c["value"] for c in sc["criteria"] if c["pred"] in ("status_is", "equals") and c["part"] == "store"]
    rec["decision_spans"] = dict(field="task_text", spans=render.decision_spans(rec["task_text"], auth))
    return rec


# ---- secondary (reason) head rows, G7: extra copies, same context, own question form and options -----------------
REASON_OPTIONS = list(perturb.REASONS) + ["none"]


def head_row(ctx, rec, pos=None):
    """The reason head as a HEAD ROW: the same rendered context, a separate question form and its own lettered options
    (the eight reasons plus `none`), gold from the same solver. Outside the family size."""
    gid = rec["group_id"]
    rng = ctx.rng("head", gid, rec["pair_role"] or "s")
    gold = rec["gold_reason"]
    pos = rng.randrange(len(REASON_OPTIONS)) if pos is None else pos
    order = util.place_gold(list(REASON_OPTIONS), gold, pos % len(REASON_OPTIONS), rng)
    letters = render.letter_options([tw.REASON_TEXT[r] for r in order])
    opts = [dict(label=r, text=t, letter=L) for r, (L, t) in zip(order, letters)]
    h = dict(rec)
    h["head"] = True
    h["row_id"] = rec["row_id"] + "-head"
    h["options"] = opts
    h["gold"] = gold
    h["gold_letter"] = next(o["letter"] for o in opts if o["label"] == gold)
    question = "Question: What is the reason for the decision on this task?"
    otext = render.option_block(letters)
    h["rendered"] = dict(context=rec["rendered"]["context"], question=question, options_text=otext,
                         text=rec["rendered"]["context"] + "\n\n" + question + "\n" + otext)
    h["pair_role"] = None
    return h
