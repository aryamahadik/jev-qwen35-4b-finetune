"""T60 scene model (spec_k1 for T60): cards, registered edit fields, per-head edit functions, line-kind ownership. CODE ONLY.

A scene is plain JSON-able data. Common: spec_id, family T60, head h1|h2|h3, block, view, world tool|repo, card {id, slots}, ent {...},
alarm, levels. Head-specific (the gold reads ONLY these):
  h1  brief {steps [..], files [{path, tokens}], result_tokens, needs [handle], writes [res], incoming [pending step id]},
      main {facts [{handle, value}], pending [{id, reads [res], writes [res]}]}
  h3  steps [{sid, verb, entity, target, effect}], edges [[a, b]] (the DAG: b uses the output of a), stated_edges [[a, b]] (order statements
      of the request)
  h2  facts [{id, type V|R|D|S|P, handle, entity, value, idx, markers, art, content_of}], plan [{sid, status, refs, cond_host, ...}], quote
Tags (head, edit field, level, quad cell, markers) are written by the generator, read by the gates, never rendered.
"""
import copy

import t60_rule as rule

FAMILY = "T60"
HEADS = ("h1", "h2", "h3")
HEAD_IDS = {"h1": "head.t60.delegate", "h2": "head.t60.keep", "h3": "head.t60.plan"}
HEAD_LABELS = {"h1": rule.H1_LABELS, "h2": rule.H2_LABELS, "h3": rule.H3_LABELS}

CARDS = {
    "card.t60.d01": dict(head="h1", S_min=3, V=4000, B_max=2, R_max=400),
    "card.t60.d02": dict(head="h1", S_min=4, V=8000, B_max=1, R_max=200),
    "card.t60.d03": dict(head="h1", S_min=5, V=16000, B_max=3, R_max=800),
    "card.t60.d04": dict(head="h1", S_min=6, V=8000, B_max=2, R_max=400),
    "card.t60.k01": dict(head="h2", counts_recovery=True),
    "card.t60.k02": dict(head="h2", counts_recovery=False),
    "card.t60.p01": dict(head="h3", n_min=3, H=5),
    "card.t60.p02": dict(head="h3", n_min=4, H=10),
    "card.t60.p03": dict(head="h3", n_min=5, H=20),
    "card.t60.p04": dict(head="h3", n_min=4, H=5),
}
CARDS_BY_HEAD = {h: tuple(c for c, v in CARDS.items() if v["head"] == h) for h in HEADS}


def card_ref(cid):
    c = dict(CARDS[cid])
    c["id"] = cid
    return c


EDIT_IDS = {
    "size_below": "edit.t60.size_below", "coupling": "edit.t60.coupling", "result_unbounded": "edit.t60.result_unbounded",
    "shared_write": "edit.t60.shared_write", "pending_dep": "edit.t60.pending_dep", "card_swap": "edit.t60.card_swap",
    "markers": "edit.t60.markers", "plan_ref": "edit.t60.plan_ref", "pointer_content": "edit.t60.pointer_content",
    "supersede": "edit.t60.supersede", "step_done": "edit.t60.step_done", "card_swap_recovery": "edit.t60.card_swap_recovery",
    "undo_added": "edit.t60.undo_added", "step_count": "edit.t60.step_count", "order_stated": "edit.t60.order_stated",
}
EDITS_BY_HEAD = {
    "h1": ("size_below", "coupling", "result_unbounded", "shared_write", "pending_dep", "card_swap"),
    "h2": ("markers", "plan_ref", "pointer_content", "supersede", "step_done", "card_swap_recovery"),
    "h3": ("undo_added", "step_count", "order_stated", "card_swap"),
}
# line kinds an edit may change between the members of a group (a card swap: the card lines only)
EDIT_OWNS = {
    "size_below": {"h1_step", "h1_file"}, "coupling": {"h1_need", "h1_main"}, "result_unbounded": {"h1_result"}, "shared_write": {"h1_pending"},
    "pending_dep": {"h1_incoming", "h1_file", "h1_pending"}, "markers": {"h2_fact", "h2_quote"}, "plan_ref": {"h2_planref"}, "pointer_content": {"h2_quote"},
    "supersede": {"h2_quote"}, "step_done": {"h2_planref"}, "undo_added": {"h3_step"}, "step_count": {"h3_step", "h3_flow", "h3_order"},
    "order_stated": {"h3_order"},
}
# salience markers (closed). mark.t60.user_source / .recency change the fact type or the position: never quad edits (T60-B10)
MARKERS = ("mark.t60.emphasis", "mark.t60.magnitude", "mark.t60.ident", "mark.t60.repeat", "mark.t60.user_source", "mark.t60.recency")
QUAD_MARKERS = ("mark.t60.emphasis", "mark.t60.magnitude", "mark.t60.ident", "mark.t60.repeat")
QUAD_CELLS = {(True, True): "quad.t60.imp_needed", (True, False): "quad.t60.imp_unneeded", (False, True): "quad.t60.bland_needed",
              (False, False): "quad.t60.bland_unneeded"}
FACT_TYPE_IDS = {"V": "fact.t60.value", "R": "fact.t60.result", "D": "fact.t60.decision", "S": "fact.t60.state", "P": "fact.t60.pointer"}
REF_IDS = {1: "ref.t60.handle", 2: "ref.t60.role", 3: "ref.t60.ordinal", 4: "ref.t60.chain"}

# repo-world step vocabulary: program -> effect kind
REPO_PROGS = {"rm": "delete", "mv": "move", "cp": "create", "mkdir": "create", "touch": "create"}
TOOL_VERBS = {"delete": ("delete", "restore"), "archive": ("update", "restore"), "rename": ("update", "restore"),
              "update": ("update", "restore"), "send": ("send", None), "export": ("publish", None), "create": ("create", "delete"),
              "reserve": ("reserve", "release"), "schedule": ("schedule", "cancel")}
EXTERNAL_VERBS = ("send", "export")


class EditNotApplicable(ValueError):
    pass


def _need(cond, why):
    if not cond:
        raise EditNotApplicable(why)


def scene_gold(scene):
    return {"h1": rule.h1_label, "h2": rule.h2_label, "h3": rule.h3_label}[scene["head"]](scene)


def twin(scene, edit, rng, **kw):
    s2 = copy.deepcopy(scene)
    EDIT_FNS[edit](s2, rng, **kw)
    return s2


# ======================================================================================================================
# H1 edits (each flips exactly ONE predicate; the other three hold on both members)
# ======================================================================================================================
def _h1_fail_size(scene, rng):
    c, b = scene["card"], scene["brief"]
    keep = max(1, c["S_min"] - 1 - scene.get("margin", 0))
    b["steps"] = b["steps"][:keep]
    per = max(1, (c["V"] - 1 - scene.get("margin", 0) * 300) // max(1, len(b["files"]) or 1))
    for f in b["files"]:
        f["tokens"] = min(f["tokens"], per // 2)
    assert rule.h1_predicates(scene)["size"] is False, rule.h1_predicates(scene)


def h1_size_below(scene, rng):
    _need(rule.h1_predicates(scene)["size"], "SIZE must hold in the base")
    _h1_fail_size(scene, rng)


def h1_coupling(scene, rng):
    c, b = scene["card"], scene["brief"]
    handles = [f["handle"] for f in scene["main"]["facts"]]
    spare = [h for h in handles if h not in b["needs"]]
    want = c["B_max"] + 1 + scene.get("margin", 0) - len(b["needs"])
    _need(len(spare) >= want, "the main thread holds too few spare facts")
    b["needs"] = b["needs"] + spare[:want]


def h1_result_unbounded(scene, rng):
    c, b = scene["card"], scene["brief"]
    b["result_tokens"] = c["R_max"] + 1 + scene.get("margin", 0) * 80 + rng.randint(0, 30)


def h1_shared_write(scene, rng):
    b, main = scene["brief"], scene["main"]
    _need(b["writes"] and main["pending"], "needs a written resource and a pending main step")
    res = b["writes"][0]
    p = main["pending"][0]
    if res not in p["reads"]:
        p["reads"] = p["reads"] + [res]


def h1_pending_dep(scene, rng):
    b, main = scene["brief"], scene["main"]
    _need(main["pending"], "needs a pending main step")
    b["incoming"] = [main["pending"][-1]["id"]]


def h1_card_swap(scene, rng, to_card=None):
    _need(to_card is not None, "the target card is chosen by the builder")
    scene["card"] = card_ref(to_card)


# ======================================================================================================================
# H3 edits
# ======================================================================================================================
def _irrev_steps(scene):
    return [s for s in scene["steps"] if rule.irrev(s["effect"], scene["card"]["H"])]


def h3_undo_added(scene, rng):
    irr = _irrev_steps(scene)
    _need(len(irr) == 1, "exactly one high-stakes step")
    e = irr[0]["effect"]
    _need(not e.get("external") and e["magnitude"] < scene["card"]["H"] and e["kind"] != "create", "the cause must be a missing undo path")
    if scene["world"] == "repo":
        e["backup"] = True
    else:
        e["undo"] = dict(tool="restore", remaining=rng.randint(7, 60))


def h3_step_count(scene, rng, remove=None):
    """Remove filler steps (and the edges / order lines they carry) until the task has n_min - 1 steps."""
    n_min = scene["card"]["n_min"]
    fill = [s for s in scene["steps"] if s.get("filler")]
    need = len(scene["steps"]) - (n_min - 1)
    _need(0 < need <= len(fill), "not enough filler steps to cross n_min")
    gone = {s["sid"] for s in fill[-need:]}
    scene["steps"] = [s for s in scene["steps"] if s["sid"] not in gone]
    scene["edges"] = [e for e in scene["edges"] if e[0] not in gone and e[1] not in gone]
    scene["stated_edges"] = [e for e in scene["stated_edges"] if e[0] not in gone and e[1] not in gone]


def h3_order_stated(scene, rng):
    implied = rule._closure([tuple(e) for e in scene["stated_edges"]])
    miss = [e for e in scene["edges"] if tuple(e) not in implied]
    _need(len(miss) == 1, "exactly one unstated ordering dependency")
    scene["stated_edges"] = scene["stated_edges"] + [list(miss[0])]


def h3_card_swap(scene, rng, to_card=None):
    _need(to_card is not None, "the target card is chosen by the builder")
    scene["card"] = card_ref(to_card)


# ======================================================================================================================
# H2 edits
# ======================================================================================================================
def fact(scene, fid):
    return rule.fact_by_id(scene, fid)


def h2_markers(scene, rng, on=None):
    """Add or remove the four quad markers (emphasis, magnitude, ident, repeat) on the quoted fact. `on` is the target set."""
    f = fact(scene, scene["quote"])
    _need(on is not None, "the target marker set is chosen by the builder")
    keep = [m for m in f["markers"] if m not in QUAD_MARKERS]
    f["markers"] = keep + sorted(on)


def h2_plan_ref(scene, rng, needed=None):
    """Make a todo step take the quoted fact (needed) or take another fact instead (unneeded). The star step is the one that carries it."""
    star = next(s for s in scene["plan"] if s["sid"] == scene["star"])
    spare = next(r for r in scene["spare_refs"])
    if needed:
        star["refs"] = [scene["star_ref"]] + [r for r in star["refs"] if r is not scene["star_ref"]][:0]
    else:
        star["refs"] = [spare]


def h2_pointer_content(scene, rng, quote=None):
    _need(quote is not None, "which one is quoted")
    scene["quote"] = quote


def h2_supersede(scene, rng, quote=None):
    _need(quote is not None, "which revision is quoted")
    scene["quote"] = quote


def h2_step_done(scene, rng, status=None):
    s = next(s for s in scene["plan"] if s["sid"] == scene["star"])
    s["status"] = status


def h2_card_swap_recovery(scene, rng, to_card=None):
    _need(to_card is not None, "the target card")
    scene["card"] = card_ref(to_card)


EDIT_FNS = {"size_below": h1_size_below, "coupling": h1_coupling, "result_unbounded": h1_result_unbounded, "shared_write": h1_shared_write,
            "pending_dep": h1_pending_dep, "card_swap": None, "markers": h2_markers, "plan_ref": h2_plan_ref,
            "pointer_content": h2_pointer_content, "supersede": h2_supersede, "step_done": h2_step_done,
            "card_swap_recovery": h2_card_swap_recovery, "undo_added": h3_undo_added, "step_count": h3_step_count,
            "order_stated": h3_order_stated}
