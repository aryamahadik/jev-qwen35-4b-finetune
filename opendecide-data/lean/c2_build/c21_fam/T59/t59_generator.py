"""T59 ASK-OR-PROCEED generator (CODE ONLY: no rows are written by this module; `generate_in_memory` returns records for unit tests and
the 20-example dry run only). Built from G0_LITE.md (batch-1b rulings) only.

Plan (G0-lite section 4, 2,000 rows): block A trigger pairs (Q-MID) 900, B early-gate pairs (Q-EARLY) 280, C card-swap pairs 140,
D controls 680 (D1 unambiguous 240 PROCEED, D2 settled 140 PROCEED, D3 reversible ambiguity 120 PROCEED, D4 clear ASK 180). The
A12 perturbation rows (150 at 2,000 rows) are DERIVED from kept clean rows by the pipeline hook (`extra_rows`), so the main plan is
sized `total - n_a12`; A10 wrapper rows (100) only when `a10=True` (decided by the Fri 23 probe, GV1).

Names: ids come from the frozen allow-list (names guard in the pipeline), display names from namespace.py via KNameSource.
"""
import collections
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from tool_engine import util  # noqa: E402
import t59_build as B  # noqa: E402
import t59_render as R  # noqa: E402
import t59_scene as sc  # noqa: E402
import t59_solver_a as sa  # noqa: E402
from t59_build import Ctx, SceneReject  # noqa: E402,F401

FAMILY = "T59"
TOTAL = 2000
A_PAIRS = {"T1": 70, "T2": 70, "T3": 50, "T4": 60, "T5": 50, "T6": 55, "T7": 50, "T8": 45}
B_PAIRS = {"T1": 30, "T2": 30, "T3": 20, "T4": 25, "T5": 15, "T7": 20}
C_SWAPS = {"T1": 15, "T2": 15, "T3": 10, "T5": 10, "T7": 10, "T8": 10}
D_ASK = {"T1": 31, "T2": 31, "T3": 22, "T4": 23, "T5": 21, "T6": 15, "T7": 22, "T8": 15}
D_PROC = {"T1": 87, "T2": 88, "T3": 60, "T4": 65, "T5": 56, "T6": 42, "T7": 60, "T8": 42}
# ---- D controls (G0-lite section 4, rows at 2,000): D1 unambiguous 240 PROCEED (80 of them in Q-EARLY form, 120 with an alarming surface),
# D2 settled by default / precedence / resolver 140 PROCEED, D3 ambiguous but all undoable (ON cards) 120 PROCEED, D4 clear ASK 180.
# Opus ruling Q2 follow-up (18 Oct 2026, before any pool rows): these numbers BIND (FU2). An earlier build had 174 / 226 / 100 and Q-EARLY 50;
# that was an unrecorded builder deviation and is reverted. The per-trigger D PROCEED totals (D_PROC) and ASK counts (D_ASK) are unchanged;
# how a trigger's D PROCEED rows split into D1 / D2 / D3 is a generator quota parameter (G0-lite section 13), fixed here before any pilot.
D1_TOTAL, D2_TOTAL, D3_TOTAL, D1_EARLY_TOTAL = 240, 140, 120, 80
D_SPLIT = {"ctl.t59.unambiguous": 0.48, "ctl.t59.settled": 0.28, "ctl.t59.reversible_ambiguity": 0.24}       # = 240 / 140 / 120 of 500
EARLY_TRIGGERS = ("T1", "T2", "T3", "T4", "T5", "T7")
# D3. Opus ruling Q2: G0-lite 3.3.1 makes the T6 'reversible ambiguity' cases ASK on every card, so T6 has NO D3 controls. FU1: the 120 stay,
# split over the seven other triggers in proportion to D_PROC, T4 and T5 weighted DOUBLE. Design reason (set before the pilot, not tuned on pilot
# numbers): T4 and T5 have no robust PROCEED form (their PROCEED side is always 'ON card, every candidate undoable'), so a D3 row there adds
# nothing to the K30 reversibility share, while a D3 row in T1, T2, T3, T7 or T8 adds one 'on_reversible' row (a plain proportional split gave
# 0.403 on a dry run against the 0.40 bar). K30 itself is judged on the built pilot rows.
D3_TRIGGERS = tuple(t for t in sc.TRIGGERS if t != "T6")
D3_WEIGHT_BOOST = {"T4": 2.0, "T5": 2.0}
# D2 (settled by default, precedence or resolver). Only mechanisms the K30 'settled' count recognises (e2 default, e10 precedence, e14 / e18
# resolver) plus the common-step cases (e8) that K30's R-COM share (>= 8%) needs: T1 e2, T3 e10, T6 e18, T7 e14 / e10, T2 / T8 e8. T4 and T5 have
# none of these mechanisms (their PROCEED side is the reversibility edit), so their D PROCEED rows are D1 and D3 only.
D2_BY_TRIGGER = {"T1": 24, "T2": 25, "T3": 18, "T4": 0, "T5": 0, "T6": 24, "T7": 24, "T8": 25}
EDIT_WEIGHTS = {
    # A + B pairs. K12: >= 3 fields per trigger, none above 40% (kept <= 38%, the allocation rounds), every field >= 2%. FU2: the weights of the
    # edits that make the PROCEED member 'settled by default / precedence / resolver' (e2, e10, e14, e18) are raised to reach the K30 bar of 15%.
    "T1": {"e1": .16, "e2": .38, "e3": .16, "e4": .14, "e5": .16}, "T2": {"e3": .15, "e5": .17, "e6": .15, "e7": .15, "e8": .38},
    "T3": {"e3": .28, "e9": .34, "e10": .38}, "T4": {"e3": .38, "e4": .38, "e11": .24}, "T5": {"e3": .34, "e12": .33, "e13": .33},
    "T6": {"e17": .20, "e18": .38, "e19": .21, "e20": .21}, "T7": {"e3": .10, "e10": .36, "e14": .38, "e15": .16},
    "T8": {"e3": .26, "e8": .38, "e16": .36},
}
TOOL_ONLY_EDITS = {"e2": ("T1",), "e4": ("T1",), "e11": ("T4",)}                 # e4 on T4 may use the repo world (H=5 card); e4 on T1 may not
REPO_TRIGGERS = ("T1", "T2", "T4", "T8")
P_REPO = 0.70
P_WORLD_W = 0.22                                                     # extra with-outputs share on top of the forced T6 / T8 rows
OFF_P = dict(pair=0.30, single_proceed=0.45, single_ask=0.15)
MECHS = ("certainty", "intent", "slot", "undo", "stakes", "resolver", "length")
MECHS_BY_TRIGGER = {"T1": ("certainty", "stakes", "undo", "length"), "T2": ("certainty", "stakes", "undo", "length"),
                    "T3": ("stakes", "undo", "length"), "T4": ("certainty", "stakes", "undo", "length"),
                    "T5": ("stakes", "undo", "length"), "T6": ("stakes", "undo", "length"), "T7": ("stakes", "undo", "length"),
                    "T8": ("certainty", "stakes", "undo", "length")}
ROW_LEVEL_P = (0.30, 0.38, 0.22, 0.10)
DECOY_ROLES = ("label", "note", "priority", "owner", "version", "reason", "mode", "limit")
N_A12_PER_2000 = {"A": 90, "B": 30, "D": 30}
N_A10_PER_2000 = {"A": 60, "B": 20, "C": 20}


def n_levers(total, a10=False):
    a12 = {k: int(round(v * total / float(TOTAL))) for k, v in N_A12_PER_2000.items()}
    a10_ = {k: int(round(v * total / float(TOTAL))) for k, v in N_A10_PER_2000.items()} if a10 else {}
    return a12, a10_


# =============================================================================================================
# plan
# =============================================================================================================
def _d_tables():
    """-> (D1, D3, D1 early) rows per trigger at 2,000 (D2 is the parameter D2_BY_TRIGGER), with the G0-lite section 4 totals asserted."""
    w = {tr: D_PROC[tr] * D3_WEIGHT_BOOST.get(tr, 1.0) for tr in D3_TRIGGERS}
    d3 = {tr: 0 for tr in sc.TRIGGERS}
    d3.update(util.largest_remainder(D3_TOTAL, w))
    d2 = dict(D2_BY_TRIGGER)
    d1 = {tr: D_PROC[tr] - d3[tr] - d2[tr] for tr in sc.TRIGGERS}
    early = {tr: 0 for tr in sc.TRIGGERS}
    early.update(util.largest_remainder(D1_EARLY_TOTAL, {tr: d1[tr] for tr in EARLY_TRIGGERS}))
    assert (sum(d1.values()), sum(d2.values()), sum(d3.values()), sum(early.values())) == (D1_TOTAL, D2_TOTAL, D3_TOTAL, D1_EARLY_TOTAL), \
        (sum(d1.values()), sum(d2.values()), sum(d3.values()), sum(early.values()))
    assert all(v >= 0 for t in (d1, d2, d3, early) for v in t.values()) and d3["T6"] == 0
    assert all(early[tr] <= d1[tr] for tr in sc.TRIGGERS) and early["T6"] == early["T8"] == 0
    assert sum(D_PROC.values()) == D1_TOTAL + D2_TOTAL + D3_TOTAL == 500 and sum(D_ASK.values()) == 180
    return d1, d3, early


D1_BY_TRIGGER, D3_BY_TRIGGER, D1_EARLY_BY_TRIGGER = _d_tables()


def _entries():
    """name -> dict(rows at 2,000, size, ...). One entry per (block, trigger, kind)."""
    ent = {}
    for tr, n in A_PAIRS.items():
        ent["A|%s|pair" % tr] = dict(block="A", trigger=tr, kind="pair", size=2, rows=2 * n, form="mid")
    for tr, n in B_PAIRS.items():
        ent["B|%s|pair" % tr] = dict(block="B", trigger=tr, kind="pair", size=2, rows=2 * n, form="early")
    for tr, n in C_SWAPS.items():
        ent["C|%s|swap" % tr] = dict(block="C", trigger=tr, kind="swap", size=2, rows=2 * n, form="mid")
    for tr in sc.TRIGGERS:
        k1e = D1_EARLY_BY_TRIGGER[tr]
        for name, ctl, k, form in (("unambiguous_early", "ctl.t59.unambiguous", k1e, "early"),
                                   ("unambiguous", "ctl.t59.unambiguous", D1_BY_TRIGGER[tr] - k1e, "mid"),
                                   ("settled", "ctl.t59.settled", D2_BY_TRIGGER[tr], "mid"),
                                   ("reversible_ambiguity", "ctl.t59.reversible_ambiguity", D3_BY_TRIGGER[tr], "mid")):
            if k > 0:
                ent["D|%s|%s" % (tr, name)] = dict(block="D", trigger=tr, kind="single", size=1, rows=k, label="PROCEED", ctl=ctl, form=form)
        ent["D|%s|ask" % tr] = dict(block="D", trigger=tr, kind="single", size=1, rows=D_ASK[tr], label="ASK",
                                    ctl="ctl.t59.clear_ask", form="mid")
    return ent


ENTRIES = _entries()


def alloc(rows_total, entries):
    raw = util.largest_remainder(rows_total, {k: v["rows"] for k, v in entries.items()})
    groups, left = {}, 0
    for k, v in entries.items():
        g = raw[k] // v["size"]
        groups[k] = g
        left += raw[k] - g * v["size"]
    singles = [k for k, v in entries.items() if v["size"] == 1]
    if left and singles:
        extra = util.largest_remainder(left, {k: entries[k]["rows"] for k in singles})
        for k, v in extra.items():
            groups[k] += v
    return groups


def _flags(n, p, rng):
    """n booleans with exactly round(n*p) True, in random order (balanced; no drift between cells)."""
    k = int(round(n * p))
    a = [True] * k + [False] * (n - k)
    rng.shuffle(a)
    return a


def build_plan(total=TOTAL, seed="t59-plan-v1", a10=False):
    """Group specs. Exact block / trigger sizes (largest remainder); edit mix per trigger; card, world, view, form, levels, alarm,
    decoy and gold-position assignments are balanced cycles, not independent draws."""
    a12, a10_ = n_levers(total, a10)
    main_total = total - sum(a12.values()) - sum(a10_.values())
    groups_n = alloc(main_total, ENTRIES)
    plan = []
    for name, e in ENTRIES.items():
        for i in range(groups_n[name]):
            g = dict(gid="%s-%s-%05d" % (e["block"], e["trigger"], i) if e["kind"] != "single" else
                     "D-%s-%s-%05d" % (e["trigger"], name.split("|")[-1], i),
                     block=e["block"], trigger=e["trigger"], kind=e["kind"], form=e["form"], size=e["size"], entry=name,
                     spec=dict(size=e["size"], name=name))
            if e["kind"] == "single":
                g.update(label=e["label"], ctl=e["ctl"])
            plan.append(g)
    rng = util.rng_for(seed, "order")
    rng.shuffle(plan)
    byc = collections.defaultdict(list)
    for g in plan:
        byc[g["entry"]].append(g)
    # ---- edits: per trigger over ALL its pair groups (K12: each edit field <= 40% of the trigger's pairs, >= 3 fields)
    for tr in sc.TRIGGERS:
        pairs = [g for g in plan if g["trigger"] == tr and g["kind"] == "pair"]
        if not pairs:
            continue
        cnt = util.largest_remainder(len(pairs), EDIT_WEIGHTS[tr])
        seq = [e for e, n in cnt.items() for _ in range(n)]
        util.rng_for(seed, "edit", tr).shuffle(seq)
        for g, e in zip(pairs, seq):
            g["edit"] = e
    # ---- order of the members of a pair (which is 'a'), balanced per trigger
    for tr in sc.TRIGGERS:
        pg = [g for g in plan if g["trigger"] == tr and g["kind"] in ("pair", "swap")]
        fl = _flags(len(pg), 0.5, util.rng_for(seed, "order-ab", tr))
        for g, f in zip(pg, fl):
            g["labels"] = ("ASK", "PROCEED") if f else ("PROCEED", "ASK")
    # ---- world
    for tr in sc.TRIGGERS:
        gs = [g for g in plan if g["trigger"] == tr]
        if tr not in REPO_TRIGGERS:
            for g in gs:
                g["world"] = "tool"
            continue
        elig = [g for g in gs if tr not in TOOL_ONLY_EDITS.get(g.get("edit"), ())]
        fl = _flags(len(elig), min(1.0, P_REPO * len(gs) / max(1, len(elig))), util.rng_for(seed, "world", tr))
        for g in gs:
            g["world"] = "tool"
        for g, f in zip(elig, fl):
            g["world"] = "repo" if f else "tool"
    # ---- view (P / W), form is fixed by the entry
    forced_w = ("T6", "T8")
    for tr in sc.TRIGGERS:
        gs = [g for g in plan if g["trigger"] == tr]
        if tr in forced_w:
            for g in gs:
                g["view"] = "with_outputs"
            continue
        fl = _flags(len(gs), P_WORLD_W, util.rng_for(seed, "view", tr))
        for g, f in zip(gs, fl):
            g["view"] = "with_outputs" if f else "primary"
    # ---- the one edit each unpaired PROCEED control is built from (decided here so that the card can satisfy it)
    import t59_build as _b
    for g in plan:
        if g["kind"] == "single" and g.get("label") == "PROCEED" and g["ctl"] in ("ctl.t59.unambiguous", "ctl.t59.settled"):
            lst = list((_b.UNAMBIGUOUS_EDITS if g["ctl"] == "ctl.t59.unambiguous" else _b.SETTLED_EDITS)[g["trigger"]])
            r = util.rng_for(seed, "ctl-edit", g["gid"])
            w = [3.0] + [1.0] * (len(lst) - 1)
            g["ctl_edit"] = r.choices(lst, w)[0]
            if g["trigger"] in TOOL_ONLY_EDITS.get(g["ctl_edit"], ()) and g["world"] == "repo":
                g["world"] = "tool"
    # ---- cards
    _assign_cards(plan, seed)
    # ---- levels, alarm, decoys, gold positions
    _assign_levels(plan, seed)
    _assign_alarm(plan, seed)
    _assign_positions(plan, seed)
    for g in plan:
        g.setdefault("labels", None)
    return plan


def _card_pool(g):
    """Card ids a group may use, from its edit / kind / world constraints."""
    edit, tr = g.get("edit") or g.get("ctl_edit"), g["trigger"]
    pool = list(sc.CARDS)
    if edit in sc.ON_ONLY_EDITS or edit == "e12" or tr == "T4" or g.get("ctl") == "ctl.t59.reversible_ambiguity":
        pool = list(sc.ON_CARDS)
    if edit == "e2":
        pool = [c for c in pool if sc.CARDS[c]["defaults_count"]]
    if edit == "e10":
        pool = [c for c in pool if sc.CARDS[c]["prec_ok"]]
    if edit in ("e14", "e18"):
        pool = [c for c in pool if sc.CARDS[c]["read_first"]]
    if edit == "e4" and g.get("world") == "repo":
        pool = [c for c in pool if sc.CARDS[c]["H"] <= 5]
    if g.get("ctl") == "ctl.t59.settled" and tr == "T1":
        pass
    return pool or list(sc.CARDS)


ASK_TARGET = 0.42                                                   # the family ASK share (G0-lite section 4): the per-card target of the greedy below


def _assign_cards(plan, seed):
    """Mode first (OFF probabilities of the design), then the card inside the mode. The card is chosen by a share-controlled greedy (build fix
    before the pilot, G0-lite section 13: K4 asks every card with >= 100 rows for an ASK share of 36-48%, and the restricted pools of the
    default / precedence / read_first edits leave c05 and c06 unevenly loaded): swap pairs first (a cycle), then the groups with the smallest
    card pools first; an ASK single (or a pair, whose ASK share is 50%) goes to the card of the pool with the lowest ASK share so far, a PROCEED
    single to the card with the highest, ties broken by the seeded stream."""
    rng = util.rng_for(seed, "cards")
    asks, rows = collections.Counter(), collections.Counter()
    cyc = [[], 0]

    def swap_draw():
        if cyc[1] >= len(cyc[0]):
            cyc[0], cyc[1] = list(range(len(sc.SWAP_PAIRS))), 0
            rng.shuffle(cyc[0])
        k = cyc[0][cyc[1]]
        cyc[1] += 1
        return k

    def share(c):
        return (asks[c] + ASK_TARGET * 4) / (rows[c] + 4.0)

    def draw(pool, want):
        jitter = {c: rng.random() * 1e-9 for c in pool}
        if want == "PROCEED":
            return min(pool, key=lambda c: (-share(c), jitter[c]))
        return min(pool, key=lambda c: (share(c), jitter[c]))

    for g in plan:
        if g["kind"] == "swap":
            g["card"], g["card_off"] = sc.SWAP_PAIRS[swap_draw()]
            rows[g["card"]] += 1                                  # the ON member (PROCEED) ...
            rows[g["card_off"]] += 1                              # ... and the OFF member (ASK)
            asks[g["card_off"]] += 1
    todo = [g for g in plan if g["kind"] != "swap"]
    pools = {id(g): _card_pool(g) for g in todo}
    todo.sort(key=lambda g: len(pools[id(g)]))                    # stable: the shuffled plan order decides within a pool size
    for g in todo:
        pool = pools[id(g)]
        off_ok = [c for c in pool if sc.CARDS[c]["mode"] == "OFF"]
        on_ok = [c for c in pool if sc.CARDS[c]["mode"] == "ON"]
        p = OFF_P["pair"] if g["kind"] == "pair" else (OFF_P["single_proceed"] if g.get("label") == "PROCEED" else OFF_P["single_ask"])
        use = off_ok if (off_ok and on_ok and rng.random() < p) else (on_ok or off_ok)
        want = g.get("label") if g["kind"] == "single" else "pair"
        g["card"] = draw(use, want)
        rows[g["card"]] += g["size"]
        asks[g["card"]] += (g["size"] if want == "ASK" else (1 if want == "pair" else 0))


def _assign_levels(plan, seed):
    for tr in sc.TRIGGERS:
        gs = [g for g in plan if g["trigger"] == tr]
        cnt = util.largest_remainder(len(gs), dict(zip(range(1, 5), ROW_LEVEL_P)))
        seq = [lv for lv, n in cnt.items() for _ in range(n)]
        util.rng_for(seed, "lvl", tr).shuffle(seq)
        for g, lv in zip(gs, seq):
            r = util.rng_for(seed, "lvlm", g["gid"])
            mechs = MECHS_BY_TRIGGER[tr]
            levels = {m: r.choice((1, 2)) for m in MECHS}
            prim = r.choice(mechs)
            levels[prim] = lv
            if lv == 4:
                second = r.choice([m for m in mechs if m != prim] or [prim])
                levels[second] = 3
            g["levels"] = levels
            g["row_level_target"] = lv
            g["prim"] = prim


def _assign_alarm(plan, seed):
    for tr in sc.TRIGGERS:
        for key in ("pair", "swap", "single_ask", "single_proceed", "d1"):
            gs = [g for g in plan if g["trigger"] == tr and _kind_key(g) == key]
            p = 0.5 if key == "d1" else 0.30
            for g, f in zip(gs, _flags(len(gs), p, util.rng_for(seed, "alarm", tr, key))):
                g["alarm"] = f
        for g in plan:
            if g["trigger"] == tr:
                r = util.rng_for(seed, "decoy", g["gid"])
                g["decoy_deleg"] = (r.choice(DECOY_ROLES) if (tr in ("T1", "T2", "T4") and g.get("edit") != "e5" and r.random() < 0.10)
                                    else None)


def _kind_key(g):
    if g["kind"] in ("pair", "swap"):
        return g["kind"]
    if g["label"] == "ASK":
        return "single_ask"
    return "d1" if g["ctl"] == "ctl.t59.unambiguous" else "single_proceed"


def _assign_positions(plan, seed):
    rows = []
    for g in plan:
        for i in range(g["size"]):
            lab = g.get("label") if g["kind"] == "single" else (g["labels"][i] if g.get("labels") else None)
            rows.append((g["gid"], i, lab))
    # the label of each member is only known once the plan is built; positions are balanced per (label) over the plan's rows
    bylab = collections.defaultdict(list)
    for gid, i, lab in rows:
        bylab[lab].append((gid, i))
    pos = {}
    for lab, items in bylab.items():
        cyc = util.balanced_cycle(len(items), 2, util.rng_for(seed, "pos", str(lab)))
        for (gid, i), p in zip(items, cyc):
            pos[(gid, i)] = p
    for g in plan:
        g["pos"] = [pos[(g["gid"], i)] for i in range(g["size"])]


# =============================================================================================================
# generation
# =============================================================================================================
MAX_ATTEMPTS = 12
TOKEN_CAP = 1450                     # G6: no row above 1,536 tokens (the proxy counter is not the real tokenizer: margin)


def generate_group(ctx, g):
    """One group -> finished records. A group the spec cannot realise is REJECTED and regenerated with the next attempt number (and,
    after a few attempts, with a fresh level draw); a solver-A disagreement with the group's intended labels is a BUILD BUG (raises)."""
    last = None
    g = dict(g)
    for attempt in range(MAX_ATTEMPTS):
        g["attempt"] = attempt
        if attempt >= 4:                                   # a stubborn draw: fall back to easy levels (the plan's target is not a gate)
            g["levels"] = dict(g["levels"], stakes=1, certainty=2, length=1)
        try:
            scenes = B.build_group(ctx, g, attempt)
        except (SceneReject, sc.EditNotApplicable, sa.SpecError) as e:
            last = e
            ctx.rejected = getattr(ctx, "rejected", 0) + 1
            continue
        recs = []
        for i, s in enumerate(scenes):
            if g["kind"] == "single":
                s["pair_role"] = None
            if g.get("edit") != "e5":
                s["decoy_deleg"] = g.get("decoy_deleg")
            recs.append(R.finalize(ctx, g, s, g["pos"][i], i))
        if any(util.approx_tokens(r["rendered"]["text"]) > TOKEN_CAP for r in recs):
            last = SceneReject("token cap")
            ctx.rejected = getattr(ctx, "rejected", 0) + 1
            continue
        if g["kind"] != "single":
            bad = pair_line_problems(recs[0], recs[1], g)
            if bad:
                last = SceneReject("pair integrity: %s" % bad)
                ctx.rejected = getattr(ctx, "rejected", 0) + 1
                continue
        for r in recs:                                     # FU5 per-row assert: scene flags, solver A and the rendered tools agree on the read path
            bad_rp = R.read_path_problems(r)
            if bad_rp:
                raise AssertionError("%s: read path: %s" % (r["row_id"], bad_rp))
        want = (g["label"],) if g["kind"] == "single" else tuple(g["labels"])
        got = tuple(r["gold"] for r in recs)
        if got != want:
            raise AssertionError("%s: solver A gave %s, the plan intends %s" % (g["gid"], got, want))
        return recs
    raise RuntimeError("group %s rejected %d times: %s" % (g["gid"], MAX_ATTEMPTS, last))



def pair_line_problems(a, b, g):
    """K14 at generation: the members differ (at all) and ONLY in line kinds the registered edit may change (a swap: card lines only)."""
    ca, cb = collections.Counter(a["lines"]), collections.Counter(b["lines"])
    diff = (ca - cb) + (cb - ca)
    if not diff:
        return ["members render identically"]
    if g["kind"] == "swap":
        allowed = None
    else:
        allowed = sc.EDIT_OWNS[g["edit"]]
    bad = []
    for (kind, _text), _n in diff.items():
        if g["kind"] == "swap":
            if not kind.startswith("card_"):
                bad.append(kind)
        elif kind not in allowed:
            bad.append(kind)
    return sorted(set(bad))


def generate_in_memory(total=20, seed="t59-dry", standin=True, ctx=None):
    """Build `total` examples IN MEMORY (unit tests / dry run only; nothing is written)."""
    ctx = ctx or Ctx(seed=seed, standin=standin)
    plan = build_plan(total=total, seed=seed)
    recs = []
    for g in plan:
        recs.extend(generate_group(ctx, g))
    return recs
