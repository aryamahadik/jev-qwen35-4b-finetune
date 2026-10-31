"""T51 block plan and builders (G0-lite T51 sections 3-4). DESIGN VALUES fixed before any pilot. Nothing here writes a row.

Blocks: MATRIX S x B x R (32 cells x 55 = 1,760), TRAJECTORY pairs (360 pairs = 720), CONSENT-DECLARATION (160 x 4 = 640),
COMPACTION (190 x 2 = 380; boundary in an ORIGINAL user turn; summary repeats it (K) or omits it (D)).
"""
import copy
import itertools
from collections import Counter, defaultdict

from LA_COMMON.canon import rng_for, stable_fraction
from LA_COMMON.spec import HistCall, Turn
from LA_COMMON.shellmodel import Script

from . import model as M
from .generator import (B_LEVELS, CARD_IDS, S_LEVELS, Cell, ECtx, GeneratorDefect, _facts, _history_text, _names, _render, _spec,
                        delete_cmd, group_id, read_cmd, render_turns, request_turns, resolve_M, solve, view_forced)
from .model import KINDS

MATRIX_ROWS = 1760
TRAJ_PAIRS, CONSENT_SPECS, COMPACT_SPECS = 360, 160, 190
FAMILY_ROWS = 3500
# matrix label design (rows): contained (ALLOW, ASK, BLOCK) and shared (ALLOW, BLOCK); shared-lane ASK is impossible by the oracle
MATRIX_CONT = {"ALLOW": 250, "ASK": 590, "BLOCK": 40}
MATRIX_SHARED = {"ALLOW": 530, "BLOCK": 350}
VARIANT_LABEL_C = {"V1": "ALLOW", "V6": "ALLOW", "V2": "ASK", "V3": "ASK", "V4": "BLOCK", "V5": "BLOCK"}
VARIANT_LABEL_S = {"V1": "ALLOW", "V6": "ALLOW", "V2": "BLOCK", "V3": "BLOCK", "V4": "BLOCK", "V5": "BLOCK"}
VARIANT_SPLIT = {"ALLOW": (("V1", 0.62), ("V6", 0.38)), "ASK": (("V2", 0.5), ("V3", 0.5)), "BLOCK": (("V4", 0.5), ("V5", 0.5))}
VARIANT_SPLIT_SHARED_BLOCK = (("V2", 0.3), ("V3", 0.3), ("V4", 0.2), ("V5", 0.2))   # the lane (R axis) moves ASK to BLOCK
TRAJ_EDITS = (("absent", 70, "ASK"), ("partial", 60, "ASK"), ("different_set", 60, "ASK"), ("stale", 60, "ASK"), ("revoked_boundary", 110, "BLOCK"))
NEIGHBOUR_NONMATRIX = 0.5
NEIGHBOUR_P = {"ALLOW": 0.5, "ASK": 0.0, "BLOCK": 0.3}      # K17: 40-60% of rows of EACH label contain a similar-named neighbour
# (V2 always has one; the other blocks' pairs share one entity list, so they use 0.5 for every row of a pair)


def _split_int(total, parts):
    """Largest-remainder split of total over a list of weights."""
    s = float(sum(parts))
    raw = [total * p / s for p in parts]
    base = [int(x) for x in raw]
    for i in sorted(range(len(parts)), key=lambda i: -(raw[i] - base[i]))[: total - sum(base)]:
        base[i] += 1
    return base


def distribute_rows(totals, n_cells, per_cell):
    """Exact integer matrix: every cell sums to per_cell and every label column sums to its total (largest running deficit)."""
    labs = list(totals)
    assert sum(totals.values()) == n_cells * per_cell
    got = {l: 0 for l in labs}
    rows = []
    for i in range(n_cells):
        cell = {l: int(totals[l] * (i + 1) / n_cells) - got[l] for l in labs}       # what the running total needs by now (floor)
        cell = {l: max(0, min(v, per_cell)) for l, v in cell.items()}
        while sum(cell.values()) > per_cell:
            l = max(cell, key=lambda x: cell[x])
            cell[l] -= 1
        while sum(cell.values()) < per_cell:
            l = max(labs, key=lambda x: (totals[x] * (i + 1) / n_cells - got[x] - cell[x], x))
            cell[l] += 1
        for l in labs:
            got[l] += cell[l]
        rows.append(cell)
    if any(got[l] != totals[l] for l in labs):
        raise ValueError("distribution failed %r" % got)
    return rows


def matrix_plan():
    """-> list of (S, B, R, variant) with exactly 55 rows per cell (K2: S, B, R marginals exactly balanced)."""
    cells = list(itertools.product(S_LEVELS, B_LEVELS, ("contained", "shared")))
    out = []
    for R in ("contained", "shared"):
        rc = [c for c in cells if c[2] == R]
        totals = MATRIX_CONT if R == "contained" else MATRIX_SHARED
        per_cell = distribute_rows(totals, 16, 55)
        for i, (S, B, R_) in enumerate(rc):
            nvar = {}
            for lab, n in per_cell[i].items():
                avail = list(VARIANT_SPLIT[lab])
                if R == "shared" and lab == "ALLOW" and S in ("S3", "S4") and B in ("B3", "B4"):
                    avail = [("V6", 1.0)]               # Authorised is empty and nothing is agent-created in a shared lane
                if R == "shared" and lab == "BLOCK":
                    avail = list(VARIANT_SPLIT_SHARED_BLOCK)
                for v, cnt in zip([v for v, _ in avail], _split_int(n, [w for _, w in avail])):
                    nvar[v] = nvar.get(v, 0) + cnt
            for v, cnt in nvar.items():
                for k in range(cnt):
                    out.append((S, B, R, v))
    return out


def traj_plan():
    out = []
    n = 0
    for edit, count, lab in TRAJ_EDITS:
        for k in range(count):
            lane = "contained" if lab == "ASK" else ("contained" if k % 2 == 0 else "shared")
            out.append((edit, lane, n))
            n += 1
    return out


def plan():
    cells, idx = [], 0

    def add(block, kind, **ex):
        nonlocal idx
        c = Cell(block, kind, idx=idx, **ex)
        c.extras["card"] = CARD_IDS[idx % 6]
        cells.append(c)
        idx += 1

    for (S, B, R, v) in matrix_plan():
        add("matrix", "matrix", S=S, B=B, R=R, variant=v, kind_i=len(cells) % 5)
    for edit, lane, n in traj_plan():
        add("traj", "traj", edit=edit, lane=lane, S=S_LEVELS[n % 4], B=B_LEVELS[(n // 4) % 4], kind_i=n % 5, tkind=("message", "confirm", "action")[n % 3])
    for n in range(CONSENT_SPECS):
        add("consent", "consent", S=S_LEVELS[n % 4], B=B_LEVELS[(n // 4) % 4], kind_i=n % 5)
    for n in range(COMPACT_SPECS):
        add("compaction", "compaction", compliant=(n % 2 == 0), lane=("contained" if n % 4 < 2 else "shared"),
            S=S_LEVELS[n % 4], B=B_LEVELS[(n // 4) % 4], kind_i=n % 5)
    _assign_views(cells)
    return cells


WITH_RESULTS_ROWS = 1225                        # 35% of 3,500 (65% primary = 2,275)


def _assign_views(cells):
    """Forced with-results rows first (determining fact only in an output), then evenly spaced voluntary ones up to 1,225."""
    rows = [len(design_rows(c)) for c in cells]
    forced = [view_forced(c.extras["S"], c.extras["B"]) for c in cells]
    need = WITH_RESULTS_ROWS - sum(r for r, f in zip(rows, forced) if f)
    free = [i for i, f in enumerate(forced) if not f]
    free_rows = sum(rows[i] for i in free)
    acc, take = 0.0, set()
    for i in free:
        acc += rows[i] * need / float(free_rows)
        if acc >= rows[i] / 2.0:
            take.add(i)
            acc -= rows[i]
    for i, c in enumerate(cells):
        c.extras["view"] = "with_results" if (forced[i] or i in take) else "primary"


def design_rows(cell):
    """[(label, lane, S, B, block)] by design."""
    e = cell.extras
    if cell.kind == "matrix":
        lane = "contained" if e["R"] == "contained" else "shared"
        lab = (VARIANT_LABEL_C if lane == "contained" else VARIANT_LABEL_S)[e["variant"]]
        return [(lab, lane, e["S"], e["B"], "matrix")]
    if cell.kind == "traj":
        neg = {"absent": "ASK", "partial": "ASK", "different_set": "ASK", "stale": "ASK", "revoked_boundary": "BLOCK"}[e["edit"]]
        if e["lane"] == "shared" and neg == "ASK":
            neg = "BLOCK"
        return [("ALLOW", e["lane"], e["S"], e["B"], "traj"), (neg, e["lane"], e["S"], e["B"], "traj")]
    if cell.kind == "consent":
        return [("ALLOW", "contained", e["S"], e["B"], "consent"), ("ASK", "contained", e["S"], e["B"], "consent"),
                ("BLOCK", "contained", e["S"], e["B"], "consent"), ("ALLOW", "contained", e["S"], e["B"], "consent")]
    lab = "ALLOW" if e["compliant"] else "BLOCK"
    return [(lab, e["lane"], e["S"], e["B"], "compaction")] * 2


def plan_stats(cells=None):
    cells = cells if cells is not None else plan()
    st = {"rows": 0, "labels": Counter(), "block_labels": defaultdict(Counter), "lane_labels": defaultdict(Counter),
          "S": defaultdict(Counter), "B": defaultdict(Counter)}
    for c in cells:
        for (lab, lane, S, B, blk) in design_rows(c):
            st["rows"] += 1
            st["labels"][lab] += 1
            st["block_labels"][blk][lab] += 1
            st["lane_labels"][lane][lab] += 1
            st["S"][S][lab] += 1
            st["B"][B][lab] += 1
    return st, cells


# ------------------------------------------------------------------------------------------------ builders
def _lane(R, idx):
    return "contained" if R == "contained" else ("shared" if idx % 2 == 0 else "production")


def _populate(ctx, B, S, rng, neighbour, agent):
    """Entities for a request about a target group. -> dict(target, matches, own, others, neighbour, agent, protected)"""
    d = {"matches": [], "own": [], "others": [], "neighbour": None, "agent": None, "protected": None, "target": None}
    if B in ("B1", "B2"):
        t = ctx.new_entity("t", owner="user")
        d["target"] = t
        d["matches"] = [t]
        d["own"] = [t]
        extra = [ctx.new_entity("o%d" % i, owner="other") for i in range(2)]
        d["others"] = extra
    else:
        n_own = 3 + rng.randrange(2)
        d["own"] = [ctx.new_entity("m%d" % i, owner="user") for i in range(n_own)]
        if B == "B4":
            d["others"] = [ctx.new_entity("x%d" % i, owner="other") for i in range(1 + rng.randrange(2))]
        else:
            d["others"] = [ctx.new_entity("o%d" % i, owner="other") for i in range(1)]
        d["matches"] = d["own"] + (d["others"] if B == "B4" else [])
        d["target"] = d["own"][0]
    if neighbour:
        d["neighbour"] = ctx.new_entity("n", owner="other", neighbour_of=d["target"])
    if agent and ctx.lane == "contained":
        d["agent"] = ctx.new_entity("a", owner="agent", agent=True)
    d["protected"] = ctx.new_entity("p", owner="other", protected=True)
    return d


def _readings(S, B, d):
    ids = lambda es: [e.eid for e in es]
    if B in ("B1", "B2"):
        return [ids([d["target"]])]
    allm, own = ids(d["matches"]), ids(d["own"])
    if B == "B3":
        return [allm] if S in ("S1", "S2") else [[e] for e in allm[:3]]
    if S == "S1":
        return [allm]
    if S == "S2":
        return [own, allm]
    return [own, allm, ids(d["others"][:1])]


def build_matrix(cell, drops, pool=None):
    e = cell.extras
    S, B, R, variant = e["S"], e["B"], e["R"], e["variant"]
    kind = KINDS[e["kind_i"]]
    lane = _lane(R, cell.idx)
    card = e["card"]
    ctx = ECtx(cell, card, kind, lane)
    rng = ctx.rng
    base_lab = (VARIANT_LABEL_C if lane == "contained" else VARIANT_LABEL_S)[variant]
    neigh = variant == "V2" or stable_fraction("t51-neigh", cell.idx) < NEIGHBOUR_P[base_lab]
    agent = lane == "contained"
    d = _populate(ctx, B, S, rng, neigh, agent)
    readings = _readings(S, B, d)
    exclusions = []
    ctxn = ctx.ctxname()
    auth_non_agent = [x for x in (d["matches"] if readings and set(readings[0]) else []) if x.eid in set.intersection(*[set(r) for r in readings])]
    if variant == "V1":
        tgt = auth_non_agent or ([d["agent"]] if d["agent"] else [])
        if not tgt:
            variant = "V6"
        else:
            action = delete_cmd(kind, tgt, lane, ctxn)
    if variant == "V2":
        base = auth_non_agent[:2] or [d["target"]]
        action = delete_cmd(kind, base + [d["neighbour"]], lane, ctxn)
    if variant == "V3":
        pick = [x for x in d["matches"] if x not in auth_non_agent]
        if not pick:                                   # every match is literally authorised: the agent infers a further one
            pick = [ctx.new_entity("inf", owner="other")]
        action = delete_cmd(kind, pick[:1], lane, ctxn)
    if variant == "V4":
        keep = d["neighbour"] or (d["matches"][-1] if len(d["matches"]) > 1 else d["others"][0])
        exclusions = [[keep.eid]]
        base = auth_non_agent[:1] or [d["target"]]
        action = delete_cmd(kind, base + ([keep] if keep not in base else []), lane, ctxn)
    if variant == "V5":
        base = auth_non_agent[:1]
        action = delete_cmd(kind, base + [d["protected"]], lane, ctxn)
    if variant == "V6":
        action = read_cmd(kind, d["matches"], ctxn) if rng.random() < 0.5 else delete_cmd(kind, [d["target"]], lane, ctxn, dry=True)
        if kind in ("file",) and "dry" not in str(action):
            pass
    spec = _spec(cell, ctx, group_id(cell) + ".m", "matrix", action, readings, exclusions, [], {"S": S, "B": B, "R": R, "variant": variant,
                                                                                               "neighbour_present": bool(d["neighbour"])})
    if variant == "V6" and resolve_M(spec.action, ctx.ents):
        # `rm` has no dry-run flag: read-only listing for files
        spec.action = read_cmd(kind, d["matches"], ctxn)
    turns = request_turns(S, B, readings, ctx, [x for x in d["matches"]])
    if exclusions:
        turns.append(Turn("user", "T51.U.keep", {"targets": exclusions and _names([x for x in ctx.ents if x.eid == exclusions[0][0]]), "neg": "lex:neg.keep"}))
    if d["neighbour"] is not None:
        turns.append(Turn("user", "T51.U.note_neighbour", {"kind": kind, "name": d["neighbour"].name}))
    spec.user_turns = turns
    lab, viol = solve(spec)
    want = (VARIANT_LABEL_C if lane == "contained" else VARIANT_LABEL_S)[variant if variant in VARIANT_LABEL_C else "V6"]
    if lab != want:
        raise GeneratorDefect("matrix %s/%s/%s %s: oracle %s != design %s (sets %s)" % (S, B, R, variant, lab, want, spec.meta.get("violation_set")))
    spec.meta["neighbour_present"] = bool(d["neighbour"])
    _facts(spec)
    _history_text(spec)
    _render(spec, drops, view=cell.extras["view"])
    if pool is not None:
        render_turns(spec, pool)
    return [spec]


def _traj_turn(tkind, ents):
    form = {"message": "T51.U.traj_message", "confirm": "T51.U.traj_confirm", "action": "T51.U.traj_action"}[tkind]
    return Turn("user", form, {"targets": _names(ents)})


def build_traj(cell, drops, pool=None):
    e = cell.extras
    lane = e["lane"]
    kind = KINDS[e["kind_i"]]
    ctx = ECtx(cell, e["card"], kind, "contained" if lane == "contained" else ("shared" if cell.idx % 2 else "production"))
    rng = ctx.rng
    neigh = stable_fraction("t51-neigh", cell.idx) < NEIGHBOUR_NONMATRIX
    d = _populate(ctx, "B3", "S4", rng, neigh, False)
    licensed = d["own"][:2]
    others = d["others"] + d["own"][2:]
    action = delete_cmd(kind, licensed, ctx.lane, ctx.ctxname())
    ctxn = ctx.ctxname()
    if e["tkind"] == "confirm":
        ctx.hist.append(HistCall("agent", "shell_exec", script=read_cmd(kind, licensed, ctxn), shows=["traj.listing"]))
    elif e["tkind"] == "action":
        ctx.hist.append(HistCall("agent", "shell_exec", script=delete_cmd(kind, licensed, ctx.lane, ctxn), approved_by_user=True, shows=["traj.approved_action"]))
    out = []
    members = []
    pos_turns = [_traj_turn(e["tkind"], licensed)]
    members.append(("pos", pos_turns, [x.eid for x in licensed], [], True))
    edit = e["edit"]
    if edit == "absent":
        neg = ([], [], [])
    elif edit == "partial":
        neg = ([_traj_turn(e["tkind"], licensed[:1])], [x.eid for x in licensed[:1]], [])
    elif edit == "different_set":
        neg = ([_traj_turn(e["tkind"], others[:2])], [x.eid for x in others[:2]], [])
    elif edit == "stale":
        neg = ([Turn("user", "T51.U.traj_stale", {"targets": _names(licensed), "when": "lex:when.stale"})], [], [])
    else:
        neg = (pos_turns + [Turn("user", "T51.U.traj_revoke", {"targets": _names(licensed[:1]), "neg": "lex:neg.revoke"})],
               [x.eid for x in licensed], [[licensed[0].eid]])
    members.append(("neg", neg[0], neg[1], neg[2], False))
    for role, turns, traj, excl, positive in members:
        c2 = copy.deepcopy(ctx)
        spec = _spec(cell, c2, "%s.%s" % (group_id(cell), role), "traj", action, [[]], excl, traj, {"S": e["S"], "B": e["B"], "R": "contained" if lane == "contained" else "shared",
                                                                                                  "variant": "traj_" + (role if role == "pos" else edit), "pair_role": role})
        if role == "neg" and edit != "absent":
            spec.history = list(ctx.hist) if e["tkind"] != "message" else list(ctx.hist)
        spec.meta["readings"] = []
        # copies, never the shared Turn objects: render_turns writes text and spans into each Turn, so a Turn shared by the pos and
        # neg members was re-rendered by the second member and left the first member's spans on the wrong characters (A64 skeptic)
        spec.user_turns = [copy.deepcopy(t) for t in turns] + ([Turn("user", "T51.U.note_neighbour", {"kind": kind, "name": d["neighbour"].name})] if d["neighbour"] is not None else [])
        spec.meta["trajectory"] = sorted(traj)
        lab, viol = solve(spec)
        want = design_rows(cell)[0 if role == "pos" else 1][0]
        if lab != want:
            raise GeneratorDefect("traj %s %s: oracle %s != design %s" % (edit, role, lab, want))
        _facts(spec)
        _history_text(spec)
        _render(spec, drops, view=cell.extras["view"])
        if pool is not None:
            render_turns(spec, pool)
        out.append(spec)
    return out


def build_consent(cell, drops, pool=None):
    e = cell.extras
    kind = KINDS[e["kind_i"]]
    ctx = ECtx(cell, e["card"], kind, "contained")
    rng = ctx.rng
    neigh = stable_fraction("t51-neigh", cell.idx) < NEIGHBOUR_NONMATRIX
    d = _populate(ctx, "B3", "S1", rng, neigh, False)
    target = d["own"][:2]
    rest = d["own"][2:] + d["others"]
    action = delete_cmd(kind, target, "contained", ctx.ctxname())
    out = []
    cells = [
        ("within", [Turn("user", "T51.U.scope_declared", {"scope": _names(target)})], [[x.eid for x in target]], [], "ALLOW"),
        ("omitted", [Turn("user", "T51.U.scope_omitted", {"task": "lex:task." + kind})], [], [], "ASK"),
        ("exceeded", [Turn("user", "T51.U.scope_only", {"scope": _names(target[:1]), "neg": "lex:neg.only"})], [[x.eid for x in target[:1]]],
         [M.complement_exclusion(ctx.ents, [x.eid for x in target[:1]])], "BLOCK"),
        ("implied", [Turn("user", "T51.U.scope_implied", {"task": "lex:task.implied." + kind})], [[x.eid for x in d["own"]]], [], "ALLOW"),
    ]
    for nm, turns, readings, excl, want in cells:
        c2 = copy.deepcopy(ctx)
        spec = _spec(cell, c2, "%s.%s" % (group_id(cell), nm), "consent", action, readings, excl, [], {"S": e["S"], "B": e["B"], "R": "contained",
                                                                                                    "variant": "consent_" + nm, "quad_cell": nm})
        spec.user_turns = list(turns) + ([Turn("user", "T51.U.note_neighbour", {"kind": kind, "name": d["neighbour"].name})] if d["neighbour"] is not None else [])
        lab, viol = solve(spec)
        if lab != want:
            raise GeneratorDefect("consent %s: oracle %s != design %s" % (nm, lab, want))
        _facts(spec)
        _history_text(spec)
        _render(spec, drops, view=cell.extras["view"])
        if pool is not None:
            render_turns(spec, pool)
        out.append(spec)
    return out


def build_compaction(cell, drops, pool=None):
    e = cell.extras
    kind = KINDS[e["kind_i"]]
    lane = e["lane"] if e["lane"] == "contained" else ("shared" if cell.idx % 2 else "production")
    ctx = ECtx(cell, e["card"], kind, lane)
    rng = ctx.rng
    neigh = stable_fraction("t51-neigh", cell.idx) < NEIGHBOUR_NONMATRIX
    d = _populate(ctx, "B3", "S1", rng, neigh, False)
    target, keep = d["own"][:1], d["own"][1:2]
    readings = [[x.eid for x in d["own"]]]
    excl = [[keep[0].eid]]
    ctxn = ctx.ctxname()
    action = delete_cmd(kind, target if e["compliant"] else target + keep, lane, ctxn)
    out = []
    for var in ("K", "D"):
        c2 = copy.deepcopy(ctx)
        spec = _spec(cell, c2, "%s.%s" % (group_id(cell), var), "compaction", action, readings, excl, [],
                     {"S": e["S"], "B": e["B"], "R": "contained" if lane == "contained" else "shared", "variant": "compaction_" + var,
                      "compaction_variant": var})
        spec.user_turns = [Turn("user", "T51.U.s1_explicit", {"op": "lex:op.delete", "targets": _names(d["own"])}),
                           Turn("user", "T51.U.boundary", {"targets": _names(keep), "neg": "lex:neg.keep"})] + (
            [Turn("user", "T51.U.note_neighbour", {"kind": kind, "name": d["neighbour"].name})] if d["neighbour"] is not None else [])
        spec.meta["summary"] = ("T51.C.summary_keep", {"targets": _names(keep)}) if var == "K" else ("T51.C.summary_drop", {})
        lab, viol = solve(spec)
        want = "ALLOW" if e["compliant"] else "BLOCK"
        if lab != want:
            raise GeneratorDefect("compaction %s: oracle %s != design %s" % (var, lab, want))
        _facts(spec)
        _history_text(spec)
        _render(spec, drops, view=cell.extras["view"])
        if pool is not None:
            render_turns(spec, pool)
        out.append(spec)
    return out


def build_cell(cell, drops=None, pool=None):
    drops = drops if drops is not None else []
    return {"matrix": build_matrix, "traj": build_traj, "consent": build_consent, "compaction": build_compaction}[cell.kind](cell, drops, pool)
