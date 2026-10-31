"""T60 scene builders: H1 DELEGATE-OR-DO, H3 PLAN-OR-ACT, H2 KEEP-OR-DROP. CODE ONLY (no rows).
`build_group(ctx, g, attempt)` -> list of scenes for one plan group (a pair, a swap pair, a quad, or a single control). Every scene's gold is
asserted with solver A (t60_rule); a pair must flip EXACTLY the intended predicate. Names are display names from namespace.py (bucket.t60).
"""
import collections
import copy
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from LK_COMMON import knames  # noqa: E402
from tool_engine import state, util  # noqa: E402
import t60_levels as lv_levels  # noqa: E402
import t60_model as M  # noqa: E402
import t60_rule as rule  # noqa: E402
import t60_wording as tw  # noqa: E402

FAMILY = "T60"


class SceneReject(RuntimeError):
    pass


# Opus ruling Q1 (18 Oct 2026, before any pool rows): a supersession chain never repeats a value. The code of the per-row creation-time drop:
SUPERSEDE_SAME_VALUE = "supersede_same_value"
ORDINAL_ON_SUPERSEDED = "ordinal_on_superseded"      # Opus ruling Q6 batch 2 (B2-1): per-row drop code, own counter, not a G13 drop
REPEAT_MARKER = "mark.t60.repeat"
MENTION_P = 0.42                          # share of quad / step-done groups whose done decoy step names the quoted fact's noun (plan level, K6)
CHAIN_REDRAWS = 64                        # redraws of one revision value before the group is rejected (46 values exist per slot; depth <= 3)


class Ctx:
    def __init__(self, seed="t60-v1", standin=False, pool=None, names_src=None):
        self.seed = seed
        self.names = names_src or knames.KNameSource(FAMILY, seed=seed, standin=standin)
        self.pool = pool or tw.seed_pool()
        self.pool.balanced = True
        self.rejected = 0
        self.drops = collections.Counter()               # per-row creation-time drops by code, counted in ROWS (the member rows of the dropped group)

    def rng(self, *parts):
        return util.rng_for(self.seed, *parts)

    def pick(self, form_id, gid, key, fallback=None):
        fid, idx, tpl = self.pool.pick(form_id, self.rng("w", gid, key), fallback, key=(gid, key))
        return fid, idx, tpl


def cat(ctx, key):
    return ctx.names.other("category", key)


def nid(rng, noun):
    return state.gen_value(rng, "str", noun)


def path_of(ctx, root, d, key, ext):
    return "%s/%s/%s%s" % (root, d, ctx.names.other("path_stem", key), ext)


def base_scene(ctx, g, rng, head):
    gid = g["gid"]
    world = g["world"]
    nn = ctx.names.draw_nouns("noun_entity", 6, gid, rng)
    ff = ctx.names.draw_nouns("noun_field", 6, gid, rng)
    sc = dict(spec_id=gid, family=FAMILY, head=head, block=g["block"], world=world,
              view="with_outputs" if head == "h2" else "primary",             # only H2 transcripts carry tool outputs (capped, data-field grammar)
              edit_ctx=None,
              alarm=bool(g.get("alarm")), levels_req=dict(g.get("levels", {})), lever=g.get("lever", "lever.none"),
              ent=dict(nouns=nn, fields=ff, unit=nn[1] if world == "tool" else "file", unit_pl=(nn[1] + "s") if world == "tool" else "files"))
    if world == "repo":
        sc["repo"] = dict(root="/work/" + ctx.names.other("repo", gid + ":root"), dir=ctx.names.other("path_stem", gid + ":dir"))
    return sc


# ======================================================================================================================
# H1
# ======================================================================================================================
def _mid(rng, lo, hi):
    return lo + (hi - lo) * rng.random()


H1_VERBS = ["read", "scan", "tally", "compare", "check", "collect", "sort"]
BOUND_D = {4: (0.0, 0.04), 3: (0.07, 0.13), 2: (0.18, 0.27), 1: (0.40, 0.75)}              # relative distance of the result from R_max, by level
VOL_R = {4: (1.01, 1.08), 3: (1.14, 1.30), 2: (1.45, 1.90), 1: (2.10, 3.00)}               # read volume / V on the volume route, by level


def h1_base(ctx, g, rng, scene):
    """The untouched part of an H1 group: a baseline brief (every mechanism easy) and the main thread. Primitives below set the levels."""
    gid = g["gid"]
    root = scene.get("repo", {}).get("root", "/work/" + ctx.names.other("repo", gid + ":r"))
    dir_a = scene.get("repo", {}).get("dir", ctx.names.other("path_stem", gid + ":d"))
    dir_b = ctx.names.other("path_stem", gid + ":d2")
    handles = ctx.names.draw_nouns("noun_field", 6, gid + ":mf", rng)
    facts = [dict(handle=handles[i], value=str(rng.randint(2, 900))) for i in range(6)]
    pend = []
    for i in range(1 if g.get("rc", {}).get("ell") == 1 else rng.randint(1, 3)):          # baseline pending steps live in ANOTHER directory (interference L1)
        pend.append(dict(id="m%d" % (i + 1), reads=["%s/%s/%s.cfg" % (root, dir_b, ctx.names.other("path_stem", "%s:pr%d" % (gid, i)))],
                         writes=["%s/%s/%s.log" % (root, dir_b, ctx.names.other("path_stem", "%s:pw%d" % (gid, i)))]))
    out = "%s/%s/%s.out" % (root, dir_a, ctx.names.other("path_stem", gid + ":out"))
    brief = dict(steps=[], files=[], result_tokens=100, needs=[], writes=[out], incoming=[])
    return dict(root=root, dir_a=dir_a, dir_b=dir_b, brief=brief, main=dict(facts=facts, pending=pend))


def _steps_text(ctx, gid, n, rng):
    return ["%s the %s" % (rng.choice(H1_VERBS), ctx.names.other("category", "%s:st%d" % (gid, i))) for i in range(n)]


def _split_files(ctx, base, gid, total, rng):
    nf = 1 if base.get("compact") else (rng.randint(1, 3) if total >= 3 else 1)
    cuts = sorted(rng.sample(range(1, max(2, total - 1)), nf - 1)) if nf > 1 and total > nf else []
    parts = [b - a for a, b in zip([0] + cuts, cuts + [total])]
    return [dict(path="%s/%s/%s.dat" % (base["root"], base["dir_a"], ctx.names.other("path_stem", "%s:in%d" % (gid, i))), tokens=int(p))
            for i, p in enumerate(parts)]


def set_size(ctx, g, base, sc, side, level, route):
    c = sc["card"]
    S, V = c["S_min"], c["V"]
    rng = util.rng_for(ctx.seed, "h1size", g["gid"], side, level, route)
    gid = g["gid"]
    small = rng.randint(120, max(130, V // 10))
    if side == "pass":
        if route == "steps":
            slack = {4: 0, 3: 1, 2: 2}.get(level) if level != 1 else rng.choice([3, 4])
            n_steps, vol = S + slack, small
        else:
            lo, hi = VOL_R[level]
            n_steps, vol = rng.randint(1, max(1, S - 1)), int(V * _mid(rng, lo, hi))
    else:
        gap = {4: 1, 3: 2, 2: 3}.get(level) if level != 1 else rng.choice([4] if S <= 5 else [4, 5])
        n_steps, vol = S - gap, small
        if n_steps < 1:
            raise SceneReject("size level %d cannot fail by %d steps with S_min %d" % (level, gap, S))
    sc["brief"]["steps"] = _steps_text(ctx, gid, n_steps, rng)
    sc["brief"]["files"] = _split_files(ctx, base, gid, vol, rng)


def set_bound(sc, side, level, rng_key):
    R = sc["card"]["R_max"]
    rng = util.rng_for(*rng_key)
    lo, hi = BOUND_D[level]
    for _ in range(40):
        d = _mid(rng, lo, hi)
        res = int(R * (1 - d)) if side == "pass" else int(R * (1 + d)) + 1
        sc["brief"]["result_tokens"] = max(10, res)
        ok_side = (res <= R) if side == "pass" else (res > R)
        if ok_side and lv_levels.bound_level(sc) == level:
            return
    raise SceneReject("no result size for bound level %d (%s)" % (level, side))


def set_needs(sc, side, level, decor, rng_key):
    B = sc["card"]["B_max"]
    rng = util.rng_for(*rng_key)
    if side == "pass":
        n = {1: 0, 3: B, 4: B}.get(level)
        if level == 2:
            n = rng.randint(1, B - 1) if B >= 2 else None
    else:
        n = {3: B + 1, 4: B + 1, 2: B + 2, 1: B + 3}[level]
    if n is None:
        raise SceneReject("coupling level %d infeasible with B_max %d" % (level, B))
    facts = sc["main"]["facts"]
    for f in facts:
        f.pop("derived_from", None)
    sc["brief"]["needs"] = [f["handle"] for f in facts[:n]]
    if decor:
        if n < 2:
            raise SceneReject("a derivable fact needs two needed facts")
        facts[n - 1]["derived_from"] = facts[0]["handle"]
        facts[n - 1]["value"] = str(rng.randint(2, 9))


def set_iff(ctx, g, base, sc, form):
    b, pend = sc["brief"], sc["main"]["pending"]
    rng = util.rng_for(ctx.seed, "h1iff", g["gid"], form)
    gid, root, da = g["gid"], base["root"], base["dir_a"]
    out = b["writes"][0]
    p0 = pend[0]
    stem = lambda k: ctx.names.other("path_stem", "%s:if:%s" % (gid, k))                    # noqa: E731
    if form == "none":
        return
    if form == "samedir":
        p0["reads"] = p0["reads"] + ["%s/%s/%s.cfg" % (root, da, stem("sd"))]
    elif form == "explicit":
        p0["reads"] = p0["reads"] + [out]
    elif form == "alias":
        base_name = out.rsplit("/", 1)[1]
        alias = ("%s/%s/./%s" % (root, da, base_name)) if rng.random() < 0.5 else ("%s/%s/%s/../%s" % (root, da, stem("sub"), base_name))
        p0["reads"] = p0["reads"] + [alias]
    elif form == "aliasdiff":
        p0["reads"] = p0["reads"] + ["%s/%s/../%s/%s.cfg" % (root, da, stem("other"), stem("ad"))]
    elif form == "declout":
        p0["writes"] = p0["writes"] + ["%s/%s/%s.new" % (root, da, stem("do"))]
    elif form == "incoming":
        b["incoming"] = [p0["id"]]
    elif form == "feed":
        path = "%s/%s/%s.in" % (root, da, stem("feed"))
        p0["writes"] = p0["writes"] + [path]
        tok = 40
        donor = max(b["files"], key=lambda f: f["tokens"])
        if donor["tokens"] > tok + 5:
            donor["tokens"] -= tok
        b["files"] = b["files"] + [dict(path=path, tokens=tok)]
    else:
        raise ValueError(form)


def h1_member(ctx, g, base, card_id, spec):
    sc = copy.deepcopy(dict(brief=base["brief"], main=base["main"]))
    full = dict(sc)
    full.update(spec_id=g["gid"], family=FAMILY, head="h1", card=M.card_ref(card_id), world=g["world"], view="primary", edit_ctx=None, block=g["block"],
                lever=g.get("lever", "lever.none"), alarm=False, ent=base["ent"], margin=0)
    if "repo" in base:
        full["repo"] = base["repo"]
    gid = g["gid"]
    side, level, route = spec["size"]
    set_size(ctx, g, base, full, side, level, route)
    set_bound(full, spec["bound"][0], spec["bound"][1], (ctx.seed, "h1bound", gid, spec["bound"][0], spec["bound"][1]))
    set_needs(full, spec["needs"][0], spec["needs"][1], spec["needs"][2], (ctx.seed, "h1needs", gid, spec["needs"][0], spec["needs"][1]))
    set_iff(ctx, g, base, full, spec["iff"])
    return full


def _h1_swap_member(ctx, g, base, card_id, shared):
    sc = copy.deepcopy(dict(brief=base["brief"], main=base["main"]))
    full = dict(sc)
    full.update(spec_id=g["gid"], family=FAMILY, head="h1", card=M.card_ref(card_id), world=g["world"], view="primary", edit_ctx=None, block=g["block"],
                lever=g.get("lever", "lever.none"), alarm=False, ent=base["ent"], margin=0)
    if "repo" in base:
        full["repo"] = base["repo"]
    rng = util.rng_for(ctx.seed, "h1swap", g["gid"])
    cards = [M.CARDS[c] for c in M.CARDS_BY_HEAD["h1"]]
    s_hi = max(c["S_min"] for c in cards)
    small = rng.randint(120, 400)
    steps = shared["steps"] if shared["bind"] == "size" else s_hi + 3
    full["brief"]["steps"] = _steps_text(ctx, g["gid"], steps, rng)
    full["brief"]["files"] = _split_files(ctx, base, g["gid"], small, rng)
    full["brief"]["result_tokens"] = shared["res"] if shared["bind"] == "bound" else rng.randint(40, 80)
    n = shared["n"] if shared["bind"] == "brief" else 0
    for f in full["main"]["facts"]:
        f.pop("derived_from", None)
    full["brief"]["needs"] = [f["handle"] for f in full["main"]["facts"][:n]]
    if shared["decor"]:
        full["main"]["facts"][n - 1]["derived_from"] = full["main"]["facts"][0]["handle"]
        full["main"]["facts"][n - 1]["value"] = str(rng.randint(2, 9))
    return full


H1_BIND = {"size_below": "size", "coupling": "brief", "result_unbounded": "bound", "shared_write": "free", "pending_dep": "free"}


def build_h1(ctx, g, rng):
    rc = g["rc"]
    scene0 = base_scene(ctx, g, rng, "h1")
    base = h1_base(ctx, g, rng, scene0)
    base["ent"] = scene0["ent"]
    base["compact"] = rc["ell"] == 1
    if "repo" in scene0:
        base["repo"] = scene0["repo"]
    kind, edit = g["kind"], g.get("edit")
    if kind == "single":
        sc = h1_member(ctx, g, base, g["card"], rc["spec"]["s"])
        _scene_check(sc, "DELEGATE" if g["ctl"] == "ctl.t60.far_inside" else "DO_HERE")
        if g["ctl"] != "ctl.t60.far_inside":
            p = rule.h1_predicates(sc)
            if sum(1 for k in ("size", "brief", "bound", "free") if not p[k]) < 2:
                raise SceneReject("multi violation fails %d predicates" % sum(1 for k in ("size", "brief", "bound", "free") if not p[k]))
        return [sc]
    if kind == "swap_card":
        shared = rc["spec"]["DELEGATE"]["shared"]
        a = _h1_swap_member(ctx, g, base, rc["spec"]["DELEGATE"]["card"], shared)
        b = _h1_swap_member(ctx, g, base, rc["spec"]["DO_HERE"]["card"], shared)
        _scene_check(a, "DELEGATE")
        _scene_check(b, "DO_HERE")
        bind = {"size": "size", "brief": "brief", "bound": "bound"}[shared["bind"]]
        if _flipped(a, b) != [bind]:
            raise SceneReject("swap flips %s, wanted %s" % (_flipped(a, b), bind))
        a["edit_ctx"] = b["edit_ctx"] = "card_swap"
        mem = {"DELEGATE": a, "DO_HERE": b}
        return [mem[x] for x in g["labels"]]
    mem = {lab: h1_member(ctx, g, base, rc["spec"][lab]["card"], rc["spec"][lab]) for lab in ("DELEGATE", "DO_HERE")}
    _scene_check(mem["DELEGATE"], "DELEGATE")
    _scene_check(mem["DO_HERE"], "DO_HERE")
    bind = H1_BIND[edit]
    if _flipped(mem["DELEGATE"], mem["DO_HERE"]) != [bind]:
        raise SceneReject("pair flips %s, wanted %s" % (_flipped(mem["DELEGATE"], mem["DO_HERE"]), bind))
    for s in mem.values():
        s["edit_ctx"] = edit
    return [mem[x] for x in g["labels"]]


def _flipped(a, b):
    pa, pb = rule.h1_predicates(a), rule.h1_predicates(b)
    return [k for k in ("size", "brief", "bound", "free") if pa[k] != pb[k]]


def _scene_check(scene, want):
    got = M.scene_gold(scene)
    if got != want:
        raise SceneReject("%s gold is %s, wanted %s" % (scene["head"], got, want))


# ======================================================================================================================
# H3
# ======================================================================================================================
H3_KIND = {"delete": "delete", "archive": "update", "rename": "update", "update": "update", "send": "send", "export": "publish", "create": "create",
           "reserve": "reserve", "schedule": "schedule", "rm": "delete", "mv": "move", "cp": "create", "mkdir": "create", "touch": "create"}
TOOL_LOW_VERBS = ("update", "archive", "rename", "reserve", "schedule", "create", "delete")        # undoable, low stakes
TOOL_DECISIVE_VERBS = ("update", "archive", "rename", "reserve", "schedule", "delete")             # a create is undoable (agent-made): never the decisive step
REPO_VERBS = ("rm", "mv", "cp", "mkdir", "touch")
R1_FORMS = ("plain", "magn", "ext", "expired")                       # the decisive step is irreversible (R1 holds)
UNDO_FORMS = ("undo_long", "undo_short")                             # the decisive step is undoable (R1 fails)


def h3_effect(rng, world, verb, form, H_lo, H_hi):
    """Effect record of one step. form None = a low-stakes step (undoable with a long window, small). Magnitudes use the smallest / largest stakes
    threshold of the cards the scene is shown under, so a card swap keeps R1 on both members."""
    kind = H3_KIND[verb]
    small = rng.randint(1, max(1, H_lo - 1))
    e = dict(kind=kind, backup=False, undo=None, external=False, magnitude=small, created_by_agent=(kind == "create"))
    if world == "repo":
        e["backup"] = form not in ("plain",)
        if form == "plain":
            e["created_by_agent"] = False
        if form == "magn":
            e["magnitude"] = rng.randint(H_hi, int(H_hi * 1.5) + 1)
        return e
    if form is None or form in ("undo_long", "undo_short", "magn", "ext", "expired"):
        if form == "undo_short":
            window = rng.randint(7, lv_levels.LONG_WINDOW - 1)
        elif form == "expired":
            window = rng.randint(3, 20)
        elif form == "ext":
            window = rng.randint(7, 60)
        else:
            window = rng.randint(lv_levels.LONG_WINDOW, 60)
        delay = (window + rng.randint(0, 6)) if form == "expired" else 0
        if kind in ("send", "publish") and form != "ext":
            raise SceneReject("a %s step has no undo path" % verb)
        if kind not in ("send", "publish") or form == "ext":
            e["undo"] = dict(tool="restore", remaining=max(0, window - delay), window=window, delay=delay)
        if form == "magn":
            e["magnitude"] = rng.randint(H_hi, int(H_hi * 1.5) + 1)
        if form == "ext":
            e["external"] = True
            if kind not in ("send", "publish"):
                raise SceneReject("external form needs a send step")
        if kind == "create":
            e["created_by_agent"] = True
        return e
    if form == "plain":
        e["created_by_agent"] = False
        return e
    raise ValueError(form)


def h3_member(ctx, g, base, spec, H_lo, H_hi):
    gid, world = g["gid"], g["world"]
    card = M.card_ref(spec["card"])
    n = spec["n"]
    steps = []
    dk = base["decisive"]
    for i in range(n):
        sid = "s%d" % (i + 1)
        s0 = base["steps"][i]
        s = dict(sid=sid, verb=s0["verb"], entity=s0["entity"], target=s0["target"], filler=(i >= base["n_core"]), effect=None)
        if "dest" in s0:
            s["dest"] = s0["dest"]
        form = spec["irrev"] if i == dk else None
        if i == dk:
            if world == "tool":
                if form == "ext":
                    s["verb"] = "send"
                elif s["verb"] in ("create", "send", "export"):
                    s["verb"] = base["decisive_verb"]
            else:
                if form == "plain" and s["verb"] not in ("rm", "mv"):
                    s["verb"] = "rm"
                    s.pop("dest", None)
                if s["verb"] not in ("mv", "cp"):
                    s.pop("dest", None)
        rng = util.rng_for(ctx.seed, "h3eff", gid, sid, form or "-", s["verb"])
        s["effect"] = h3_effect(rng, world, s["verb"], form, H_lo, H_hi)
        steps.append(s)
    ids = [s["sid"] for s in steps]
    edges = [[ids[i], ids[i + 1]] for i in range(len(ids) - 1)]
    order = spec["order"]
    form_order = "words"
    derived = [list(edges[0])] if (spec.get("derived") and edges) else []          # the first dependency runs through a derived value
    if order[0] == "unstated":
        if not edges:
            raise SceneReject("an unstated order needs two steps")
        stated = [list(e) for e in edges[1:]]
    elif order[0] == "numbered":
        stated, form_order = [list(e) for e in edges], "numbered"
    else:
        stated = [list(e) for e in edges]
    sc = dict(base["scene"])
    sc = copy.deepcopy(sc)
    sc.update(card=card, steps=steps, edges=edges, stated_edges=stated, derived_edges=derived, order_form=form_order)
    sc["goal"] = dict(verbs=[s["verb"] for s in steps])
    return sc


def h3_base(ctx, g, rng, scene, n_max):
    gid, world = g["gid"], g["world"]
    ent = scene["ent"]
    nouns = ent["nouns"]
    root = scene.get("repo", {}).get("root", "")
    n_core = 3
    steps = []
    for i in range(n_max):
        r = util.rng_for(ctx.seed, "h3skel", gid, i)
        if world == "repo":
            verb = r.choice(REPO_VERBS)
            target = "%s/%s" % (root, ctx.names.other("path_stem", "%s:t%d" % (gid, i)) + (".tmp" if verb != "mkdir" else ""))
            s = dict(verb=verb, entity=nouns[i % 3], target=target)
            if verb in ("mv", "cp"):
                s["dest"] = "%s/%s.tmp" % (root, ctx.names.other("path_stem", "%s:x%d" % (gid, i)))
        else:
            verb = r.choice(TOOL_LOW_VERBS)
            s = dict(verb=verb, entity=nouns[i % 3], target=nid(r, nouns[i % 3]))
        steps.append(s)
    dk = util.rng_for(ctx.seed, "h3dec", gid).randrange(2)
    dv = util.rng_for(ctx.seed, "h3decv", gid).choice(TOOL_DECISIVE_VERBS)
    return dict(steps=steps, n_core=n_core, decisive=dk, decisive_verb=dv, scene=scene)


def build_h3(ctx, g, rng):
    rc = g["rc"]
    scene = base_scene(ctx, g, rng, "h3")
    kind, edit = g["kind"], g.get("edit")
    cards = [M.CARDS[c] for c in M.CARDS_BY_HEAD["h3"]]
    keys = list(rc["spec"])
    n_max = max(rc["spec"][k]["n"] for k in keys)
    base = h3_base(ctx, g, rng, scene, max(n_max, 3))
    if kind == "swap_card":
        H_lo = min(c["H"] for c in cards)
        H_hi = max(c["H"] for c in cards)
    else:
        H_lo = H_hi = M.CARDS[rc["spec"][keys[0]]["card"]]["H"]
    mem = {k: h3_member(ctx, g, base, rc["spec"][k], H_lo, H_hi) for k in keys}
    if kind == "single":
        sc = mem["s"]
        _scene_check(sc, "PLAN" if g["ctl"] == "ctl.t60.far_inside" else "ACT")
        return [sc]
    _scene_check(mem["PLAN"], "PLAN")
    _scene_check(mem["ACT"], "ACT")
    p0, p1 = rule.h3_predicates(mem["PLAN"]), rule.h3_predicates(mem["ACT"])
    flipped = [k for k in ("r1", "r2", "r3") if p0[k] != p1[k]]
    want = {"undo_added": ["r1"], "step_count": ["r2"], "order_stated": ["r3"]}.get(edit, ["r2"] if kind == "swap_card" else None)
    if flipped != want:
        raise SceneReject("flips %s, wanted %s" % (flipped, want))
    for s in mem.values():
        s["edit_ctx"] = "card_swap" if kind == "swap_card" else edit
    return [mem[x] for x in g["labels"]]


# ======================================================================================================================
# H2
# ======================================================================================================================
ORD = ("first", "second", "third", "fourth", "fifth")
VERB_PLAN = ("update", "archive", "rename", "reserve", "schedule", "check", "verify", "sync", "tag", "close")


def safe_stem(name):
    """First letters of a name for id-shaped values, never a word the output lint reads as an imperative."""
    from tool_engine import render
    for cand in (name[:3], name[1:4], name[2:5], name[:2] + "x"):
        if cand.lower() not in render.IMPERATIVE_START and cand.lower() not in state._STEM_DENY:
            return cand
    return "zq" + name[:1]


def _value(rng, markers, ctx, key):
    if "mark.t60.ident" in markers:                       # skeptic fix: ident AND magnitude together show BOTH (an id with a large number)
        n = rng.randint(20000, 99999) if "mark.t60.magnitude" in markers else rng.randint(1000, 9999)
        return "%s-%d" % (safe_stem(ctx.names.other("path_stem", key)), n)
    if "mark.t60.magnitude" in markers:
        return str(rng.randint(20000, 99999))
    return str(rng.randint(2, 47))


def mk_fact(ctx, rng, gid, i, ftype, handle, entity, idx, markers, art=None, content_of=None, value=None):
    f = dict(id="f%d" % i, type=ftype, handle=handle, entity=entity, idx=idx, markers=sorted(markers), art=art, content_of=content_of)
    f["value"] = value if value is not None else _value(rng, markers, ctx, "%s:v%d" % (gid, i))
    return f


def pick_markers(rng, ftype, m, allow_repeat=True):
    """m quad markers for a fact of type `ftype` (Opus ruling Q6 e): emphasis, magnitude, ident; `repeat` (a second user turn) only on V / D facts and
    never on a supersession chain. Drawn from the same pool for both members of a group, so the count (not the kind) is the only salience cue."""
    pool = ["mark.t60.emphasis", "mark.t60.magnitude", "mark.t60.ident"]
    if allow_repeat and ftype in ("V", "D"):
        pool.append("mark.t60.repeat")
    return sorted(rng.sample(pool, m))


def snap_path(ctx, rng, root, stem, markers):
    """Value of a pointer fact: an identifier-shaped stem when it carries `ident`, a large number when it carries `magnitude`."""
    if "mark.t60.ident" in markers or "mark.t60.magnitude" in markers:
        n = rng.randint(20000, 99999) if "mark.t60.magnitude" in markers else rng.randint(1000, 9999)
        stem = "%s-%d" % (safe_stem(stem), n)
    return "%s/%s.snap" % (root, stem)


def draw_revision_value(ctx, rng, gid, k, used, markers=()):
    """Opus ruling Q1: the value of revision k+1 of a supersession chain, DIFFERENT from every earlier value of the chain (`used`), so the
    values of the whole chain are pairwise distinct (this also rules out A -> B -> A at depth 2 or 3). One draw when there is no collision
    (the stream of `rng` is then the one the plain `mk_fact` draw used); a collision only redraws."""
    taken = set(str(v) for v in used)
    for _ in range(CHAIN_REDRAWS):
        v = _value(rng, markers, ctx, "%s:v%d" % (gid, 30 + k))
        if str(v) not in taken:
            return v
    raise SceneReject("no revision value distinct from the chain after %d draws" % CHAIN_REDRAWS)


def chain_of(scene, quote=None):
    """The facts of a supersession chain: every fact with the quoted fact's handle AND entity (the role), in transcript order."""
    q = rule.fact_by_id(scene, quote if quote is not None else scene["quote"])
    return sorted([f for f in scene["facts"] if f["handle"] == q["handle"] and f["entity"] == q["entity"]], key=lambda f: f["idx"])


def supersede_row_problems(scene):
    """Per-row creation-time check (Opus ruling Q1, G0-lite section 7(a)). -> [] or [SUPERSEDE_SAME_VALUE] for a supersede row that is
    outside the spec: a later statement with the same handle and entity repeats the quoted fact's value, or the values of the chain are
    not pairwise distinct (A -> B -> A included). Not a G13 drop: the group may be regenerated with a new value draw."""
    if scene.get("h2kind") != "supersede":
        return []
    q = rule.fact_by_id(scene, scene["quote"])
    chain = chain_of(scene)
    vals = [str(f["value"]) for f in chain]
    if len(set(vals)) != len(vals) or any(str(f["value"]) == str(q["value"]) for f in chain if f["idx"] > q["idx"]):
        return [SUPERSEDE_SAME_VALUE]
    return []


def ordinal_superseded_problems(scene):
    """Per-row creation-time check (Opus ruling Q6 batch 2, B2-1). -> [(step id, ordinal)] for every L3 ordinal reference ("the <ordinal> record fetched by a
    get call") of ANY step of an H2 scene that lands on a SUPERSEDED record (a later fact has the same handle and entity). The rendered row never states the
    replacement rule, so the label of such a reference would rest on a rule the row does not show. Ordinals still COUNT superseded records as positions;
    they just must not land on one. A row with a problem is dropped and regenerated on the same skeleton (own counter, not a G13 drop)."""
    if scene.get("head") != "h2":
        return []
    rs = sorted([f for f in scene["facts"] if f["type"] == "R" and not f.get("content_of")], key=lambda x: x["idx"])
    out = []
    for st in scene.get("plan", []):
        for r in st["refs"]:
            if r.get("level") == 3 and 1 <= r["ordinal"] <= len(rs):
                f = rs[r["ordinal"] - 1]
                if rule.current_of(scene, f)["id"] != f["id"]:
                    out.append((st["sid"], r["ordinal"]))
    return out


def assert_no_repeat_on_chain(scene):
    """Opus ruling Q1 guard: no `mark.t60.repeat` on any fact of a supersession chain (the reminder turn is appended at the END of the
    transcript, so it would restate an old value after its revision). An assert, not a drop: nothing assigns it to a chain fact."""
    if scene.get("h2kind") != "supersede":
        return
    for f in chain_of(scene):
        if REPEAT_MARKER in f["markers"]:
            raise AssertionError("%s: %s carries %s on a supersession chain" % (scene["spec_id"], f["id"], REPEAT_MARKER))


def ref_for(f, level, scene_facts):
    """A reference (grammar L1..L3) to fact f."""
    if level == 1:
        return dict(level=1, handle=f["handle"])
    if level == 2:
        return dict(level=2, entity=f["entity"], ftype=f["type"])
    if level == 3:
        rs = sorted([x for x in scene_facts if x["type"] == "R" and not x.get("content_of")], key=lambda x: x["idx"])
        return dict(level=3, ordinal=[x["id"] for x in rs].index(f["id"]) + 1)
    raise ValueError(level)


def build_h2(ctx, g, rng):
    scene = base_scene(ctx, g, rng, "h2")
    sub = g["h2kind"]
    gid = g["gid"]
    world = g["world"]
    ent = scene["ent"]
    nouns, fields = ent["nouns"], ent["fields"]
    rc = g["rc"]
    ind = rc["ind"]
    dist = rc["dist"]
    m_star = rc["m"]                                        # markers on the quoted fact(s) of a pair kind (None for a quad: its cells carry 0 / 3)
    ck = g["card"]
    scene["card"] = M.card_ref(ck)
    # ---- facts: F (the star fact), a spare G taken by the star step in the unneeded cell, and 1-3 other facts
    n_other = rng.randint(1, 3)
    types = ["V", "R", "D", "S"]
    star_type = rng.choice(["V", "R", "D", "S"]) if ind != 3 else "R"      # S (a state key) is quoted too: the quote's fact type covers V R D S (P: pointer pairs)
    if ind == 2:
        star_type = rng.choice(["V", "R", "D", "S"])
    ledger = rc.get("mode") == "ledger"                     # recovery L4: a ledger key (state key) read only by a counted read-back step, with a persisted copy as decoy
    if ledger:
        star_type = "S"
    facts = []
    idx = 1
    ents = list(nouns)                                  # one entity per fact: a role description (L2) must be unambiguous
    handle_pool = list(fields)
    ms0 = pick_markers(rng, star_type, m_star or 0, allow_repeat=(sub != "supersede"))
    f_star = mk_fact(ctx, rng, gid, 1, star_type, handle_pool[0], ents[0], 0, ms0, value=None)
    facts.append(f_star)
    f_spare = mk_fact(ctx, rng, gid, 2, "R" if ind == 3 else rng.choice(["V", "R"]), handle_pool[1], ents[1], 0, [])
    facts.append(f_spare)
    for j in range(n_other):
        facts.append(mk_fact(ctx, rng, gid, 3 + j, rng.choice(["V", "R", "D", "D", "S"]), handle_pool[2 + j], ents[2 + j], 0, []))
    # ordinals need >= 2 fetched R facts when L3 is used
    if ind == 3:
        for f in facts[:3]:
            f["type"] = "R"
    scene["facts"] = facts
    scene["ledger"] = ledger
    if ledger:                                              # the decoy: the same entity was exported and read back (a persisted copy under another handle)
        root_ = scene.get("repo", {}).get("root", "/work/" + ctx.names.other("repo", gid + ":r"))
        dptr = mk_fact(ctx, rng, gid, 40, "P", "path", ents[0], 0, [], art="a2",
                       value=snap_path(ctx, rng, root_, ctx.names.other("path_stem", gid + ":snap2"), []))
        facts.extend([dptr, mk_fact(ctx, rng, gid, 41, "R", handle_pool[5], ents[0], 0, [], art="a2", content_of=dptr["id"])])
    # Planned indirection L4 is realised with the one reference form that has no handle noun and needs no chain: the pointer (G0-lite section 5,
    # "pointer vs content"). Pointer pairs use it by definition; a step-done pair drawn at L4 used to fall back to an L1 handle reference.
    pform = sub == "pointer" or (sub == "step_done" and ind == 4)
    ptr = None
    if pform:
        art = "a1"
        pm = pick_markers(rng, "P", m_star or 0)
        ptr = mk_fact(ctx, rng, gid, 20, "P", "path", ents[0], 0, pm, art=art,
                      value=snap_path(ctx, rng, scene.get("repo", {}).get("root", "/work/" + ctx.names.other("repo", gid + ":r")),
                                      ctx.names.other("path_stem", gid + ":snap"), pm))
        cont = mk_fact(ctx, rng, gid, 21, "R", handle_pool[0], ents[0], 0, pick_markers(rng, "R", m_star or 0), art=art, content_of=ptr["id"])
        facts.extend([ptr, cont])
        facts.remove(f_star)
    if sub == "supersede":
        depth = g.get("depth", 1)
        revs = [f_star]
        used = [f_star["value"]]
        rev_ms = [pick_markers(rng, f_star["type"], m_star or 0, allow_repeat=False) for _ in range(depth)]    # same count on every fact of the chain, never `repeat`
        for k in range(depth):
            v = draw_revision_value(ctx, rng, gid, k, used, rev_ms[k])      # Opus ruling Q1: all values of the chain are different
            r = mk_fact(ctx, rng, gid, 30 + k, f_star["type"], f_star["handle"], f_star["entity"], 0, rev_ms[k], value=v)
            used.append(v)
            facts.append(r)
            revs.append(r)
        scene["revs"] = [r["id"] for r in revs]
    # ---- transcript order: assign idx 1..n (a random permutation; revisions keep their order), distractors are filled by the renderer
    order = list(facts)
    rng.shuffle(order)
    if sub == "supersede":
        revs = [x for x in order if x["handle"] == f_star["handle"] and x["entity"] == f_star["entity"]]
        slots = sorted(order.index(x) for x in revs)
        by_idx = sorted(revs, key=lambda x: int(x["id"][1:]) if x is not f_star else -1)
        for pos, x in zip(slots, by_idx):
            order[pos] = x
    if pform:
        order.sort(key=lambda x: (x.get("content_of") is not None, rng.random()))      # pointer before content
        order = [x for x in order if x["type"] != "P"] + [x for x in order if x["type"] == "P"]
        order.sort(key=lambda x: 0)
        pl = [x for x in order if x["type"] == "P"][0]
        order.remove(pl)
        order.insert(rng.randrange(0, len(order) + 1), pl)
    for i, x in enumerate(order):
        x["idx"] = i + 1
    # ---- plan
    steps = []
    n_done = rng.randint(1, 2)
    spare_ref = ref_for(f_spare, 1 if ind != 3 else 3, facts)
    other_steps = []
    sid = 0

    def add(status, verb, ent_, refs, cond_host=None, kind="plain"):
        nonlocal sid
        sid += 1
        steps.append(dict(sid="s%d" % sid, status=status, verb=verb, entity=ent_, refs=refs, cond_host=cond_host, kind=kind))
        return steps[-1]

    mode = rc.get("mode")                                         # None | "k1" (counted contingency star) | "k2" (uncounted one on the DROP cells of a quad)
    with_host = sub == "recovery" or mode in ("k1", "k2", "ledger")          # a todo host stands right before a contingency star: it is one of the steps before the first use
    if sub == "recovery":
        pads = 0
    elif with_host:
        pads = {2: rng.randint(0, 1), 3: rng.randint(2, 5), 4: rng.randint(6, 8)}[max(dist, 2)]
    else:
        pads = {1: 0, 2: rng.randint(1, 2), 3: rng.randint(3, 6), 4: rng.randint(7, 9)}[dist]       # steps before the first use (section 5)
    # decoy mention: a done step names the star fact's handle noun (plan overlap for DROP rows) in about half of the specs
    coin_m = rng.random()                                         # drawn in every case: the stream of the other draws does not move
    mention_star = g["mention"] if "mention" in g else coin_m < MENTION_P
    for k in range(n_done):
        fx = f_star if (k == 0 and mention_star and sub in ("quad", "step_done", "supersede", "pointer")) else rng.choice([x for x in facts if x is not f_star] or facts)
        coin = rng.random()                                        # drawn in every case: the stream of the other draws does not move
        # a decoy chosen to name the quoted fact's noun does name it (K6: among DROP rows >= 50% mention the noun in the plan)
        add("done", rng.choice(VERB_PLAN), fx["entity"], [dict(level=1, handle=fx["handle"])] if (fx is f_star or coin < 0.6) else [])
    star = None
    scene["star_note"] = None
    refs_star = None
    if pform:
        refs_star = dict(level=4, pointer="a1")
    elif ind in (1, 2, 3):
        refs_star = ref_for(f_star, ind, facts)
    else:
        refs_star = ref_for(f_star, 1, facts)                          # level 4 (chain) is built below for the quad; pointer / supersession above
    if sub == "supersede":
        # L1 handle / L2 role description / L3 ordinal of a fetched record. The ordinal names the CURRENT record of the chain (the latest one), never a superseded
        # one (Opus ruling Q6 batch 2, B2-1); the superseded records still count as positions among the fetched records.
        refs_star = ref_for(rule.current_of({"facts": facts}, f_star), ind, facts)
    # spare "needed" steps before the star step (distance), each taking another fact
    for k in range(pads):
        fx = rng.choice([x for x in facts if x is not f_star and x.get("content_of") is None and x["type"] != "P"] or facts)
        add("todo", rng.choice(VERB_PLAN), fx["entity"], [ref_for(fx, 1, facts)] if fx["type"] != "P" else [])
    if sub in ("quad", "step_done", "supersede", "pointer"):
        if with_host:
            host = add("todo", rng.choice(VERB_PLAN), ents[1], [spare_ref])
            scene["host"] = host["sid"]
            star = add("todo", rng.choice(["restore", "check", "verify"]), f_star["entity"] if sub != "pointer" else ents[0], [refs_star],
                       cond_host=host["sid"] if mode in ("k1", "ledger") else None, kind="contingency" if mode in ("k1", "ledger") else "plain")
        else:
            star = add("todo", rng.choice(VERB_PLAN), f_star["entity"] if sub != "pointer" else ents[0], [refs_star])
    elif sub == "recovery":
        host = add("todo", rng.choice(VERB_PLAN), ents[1], [spare_ref])
        star = add("todo", rng.choice(["restore", "check", "verify"]), f_star["entity"], [ref_for(f_star, 2 if ledger else 1, facts)], cond_host=host["sid"],
                   kind="contingency")
        ind = 1
    # one more todo step taking the spare fact (so G is needed regardless)
    add("todo", rng.choice(VERB_PLAN), ents[1], [spare_ref])
    scene["plan"], scene["star"] = steps, star["sid"]
    scene["spare_ref"] = spare_ref
    scene["star_ref"] = copy.deepcopy(star["refs"][0]) if star["refs"] else None
    scene["quote"] = ptr["id"] if (pform and sub == "step_done") else (f_star["id"] if sub != "pointer" else None)
    scene["h2kind"] = sub
    # order the plan: done first (as built), then the rest in the order they were added
    for f in facts:
        f["markers"] = sorted(f["markers"])
    # ---- recency / user_source are derived
    n_ev = len(order)
    for f in facts:
        ms = set(m for m in f["markers"] if m in M.QUAD_MARKERS)
        if f["type"] in ("V", "D"):
            ms.add("mark.t60.user_source")
        if f["idx"] >= n_ev - 1:
            ms.add("mark.t60.recency")
        f["markers"] = sorted(ms)
    assert_no_repeat_on_chain(scene)
    return scene


def h2_variants(ctx, g, rng):
    """-> list of scenes for the group (a quad, a pair, or a swap)."""
    base = build_h2(ctx, g, rng)
    sub = g["h2kind"]
    out = []
    if sub == "quad":
        f = rule.fact_by_id(base, base["quote"])
        # skeptic fix: the markers of the "important-looking" cells are drawn ONCE per quad (both imp cells carry the same salience, they
        # differ only in plan_ref) and only from the markers the renderer can SHOW for this fact type (mark.t60.repeat is a second user turn:
        # V / D facts only), so the tag always equals what the row displays.
        pool_m = [m for m in M.QUAD_MARKERS if m != "mark.t60.repeat" or f["type"] in ("V", "D")]
        imp_markers = rng.sample(pool_m, 3)
        for imp in (True, False):
            for need in (True, False):
                s = copy.deepcopy(base)
                f2 = rule.fact_by_id(s, s["quote"])
                keep = [m for m in f2["markers"] if m not in M.QUAD_MARKERS]
                mk = list(imp_markers) if imp else []
                rng_local = util.rng_for(ctx.seed, "qv", g["gid"])
                # value style follows the markers (magnitude / ident change the value text)
                f2["markers"] = sorted(set(keep) | set(mk))
                f2["value"] = _value(util.rng_for(ctx.seed, "qval", g["gid"], str(imp)), f2["markers"], ctx, g["gid"] + ":qv")
                star = next(x for x in s["plan"] if x["sid"] == s["star"])
                if not need and g["rc"].get("mode") == "k2":
                    star["cond_host"], star["kind"] = s["host"], "contingency"          # F is read only by a step that runs on failure, and the card does not count it
                elif not need:
                    star["refs"] = [s["spare_ref"]]
                s["cell"] = M.QUAD_CELLS[(imp, need)]
                s["edit_ctx"] = "quad"
                s["imp"], s["need"] = imp, need
                out.append(s)
        want = ["KEEP", "DROP", "KEEP", "DROP"]
        for s, w in zip(out, want):
            got = M.scene_gold(s)
            if got != w:
                raise SceneReject("quad cell %s gold %s != %s" % (s["cell"], got, w))
        return out
    if sub == "pointer":
        ptr = next(f for f in base["facts"] if f["type"] == "P")
        cont = next(f for f in base["facts"] if f.get("content_of"))
        a, b = copy.deepcopy(base), copy.deepcopy(base)
        a["quote"], b["quote"] = ptr["id"], cont["id"]
        _scene_check(a, "KEEP")
        _scene_check(b, "DROP")
        a["edit_ctx"] = b["edit_ctx"] = "pointer_content"
        mem = {"KEEP": a, "DROP": b}
        return [mem[g["labels"][0]], mem[g["labels"][1]]]
    if sub == "supersede":
        revs = base["revs"]
        a, b = copy.deepcopy(base), copy.deepcopy(base)
        a["quote"], b["quote"] = revs[-1], revs[0]
        _scene_check(a, "KEEP")
        _scene_check(b, "DROP")
        a["edit_ctx"] = b["edit_ctx"] = "supersede"
        mem = {"KEEP": a, "DROP": b}
        return [mem[g["labels"][0]], mem[g["labels"][1]]]
    if sub == "step_done":
        a, b = copy.deepcopy(base), copy.deepcopy(base)
        for s, st in ((a, "todo"), (b, "done")):
            next(x for x in s["plan"] if x["sid"] == s["star"])["status"] = st
        _scene_check(a, "KEEP")
        _scene_check(b, "DROP")
        a["edit_ctx"] = b["edit_ctx"] = "step_done"
        mem = {"KEEP": a, "DROP": b}
        return [mem[g["labels"][0]], mem[g["labels"][1]]]
    if sub == "recovery":
        a, b = copy.deepcopy(base), copy.deepcopy(base)
        a["card"], b["card"] = M.card_ref("card.t60.k01"), M.card_ref("card.t60.k02")
        _scene_check(a, "KEEP")
        _scene_check(b, "DROP")
        a["edit_ctx"] = b["edit_ctx"] = "card_swap_recovery"
        mem = {"KEEP": a, "DROP": b}
        return [mem[g["labels"][0]], mem[g["labels"][1]]]
    raise SceneReject(sub)


def build_group(ctx, g, attempt=0):
    rng = ctx.rng("b", g["gid"], attempt)
    head = g["head"]
    if head == "h1":
        return build_h1(ctx, g, rng)
    if head == "h3":
        return build_h3(ctx, g, rng)
    return h2_variants(ctx, g, rng)
