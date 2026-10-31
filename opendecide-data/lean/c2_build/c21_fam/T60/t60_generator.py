"""T60 CONTROL-NEXT generator (CODE ONLY: no rows are written by this module; `generate_in_memory` returns records for unit tests and the
20-example dry run only). Built from G0_LITE.md (batch-1b rulings) only.

Plan (G0-lite section 4, 2,000 rows): H1 DELEGATE-OR-DO 600 (240 pairs = size_below 40, coupling 40, result_unbounded 40, shared_write 40,
pending_dep 40, card_swap 40; controls 120), H2 KEEP-OR-DROP 800 (QUAD 400 = 100 specs x 4 cells, pointer-vs-content 80, supersession 160,
step-done 120, recovery card swap 40), H3 PLAN-OR-ACT 600 (240 pairs = undo_added 60, step_count 60, order_stated 60, card_swap 60;
controls 120). The A12 perturbation rows (100 at 2,000 rows) are DERIVED from kept rows by the pipeline hook, so the main plan is sized
`total - n_a12` (A10: 80 more only when `a10=True`).
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
import t60_ballast as ballast  # noqa: E402
import t60_build as B  # noqa: E402
import t60_levels as LV  # noqa: E402
import t60_recipes as RC  # noqa: E402
import t60_model as M  # noqa: E402
import t60_render as R  # noqa: E402
from t60_build import Ctx, SceneReject  # noqa: E402,F401

FAMILY = "T60"
TOTAL = 2000
ENTRIES = {
    # name: (head, kind, edit | ctl | h2kind, rows at 2,000, rows per group)
    "h1|size_below": ("h1", "pair", "size_below", 80), "h1|coupling": ("h1", "pair", "coupling", 80),
    "h1|result_unbounded": ("h1", "pair", "result_unbounded", 80), "h1|shared_write": ("h1", "pair", "shared_write", 80),
    "h1|pending_dep": ("h1", "pair", "pending_dep", 80), "h1|card_swap": ("h1", "swap_card", "card_swap", 80),
    "h1|far_inside": ("h1", "single", "ctl.t60.far_inside", 60), "h1|multi_violation": ("h1", "single", "ctl.t60.multi_violation", 60),
    "h2|quad": ("h2", "quad", "quad", 400), "h2|pointer": ("h2", "pair", "pointer", 80), "h2|supersede": ("h2", "pair", "supersede", 160),
    "h2|step_done": ("h2", "pair", "step_done", 120), "h2|recovery": ("h2", "pair", "recovery", 40),
    "h3|undo_added": ("h3", "pair", "undo_added", 120), "h3|step_count": ("h3", "pair", "step_count", 120),
    "h3|order_stated": ("h3", "pair", "order_stated", 120), "h3|card_swap": ("h3", "swap_card", "card_swap", 120),
    "h3|far_inside": ("h3", "single", "ctl.t60.far_inside", 60), "h3|multi_violation": ("h3", "single", "ctl.t60.multi_violation", 60),
}
HEAD_ROWS = {"h1": 600, "h2": 800, "h3": 600}
GROUP_SIZE = {"pair": 2, "swap_card": 2, "single": 1, "quad": 4}
P_REPO = 0.40
MECHS = LV.MECHS
N_A12_PER_2000 = {"h1": 35, "h2": 30, "h3": 35}
N_A10_PER_2000 = {"h1": 30, "h2": 20, "h3": 30}
N_DEV_PER_2000 = {"transform": 30, "wrapper": 30}
LABELS = {"h1": ("DELEGATE", "DO_HERE"), "h2": ("KEEP", "DROP"), "h3": ("PLAN", "ACT")}


def n_levers(total, a10=False):
    a12 = {k: int(round(v * total / float(TOTAL))) for k, v in N_A12_PER_2000.items()}
    a10_ = {k: int(round(v * total / float(TOTAL))) for k, v in N_A10_PER_2000.items()} if a10 else {}
    return a12, a10_


def _flags(n, p, rng):
    k = int(round(n * p))
    a = [True] * k + [False] * (n - k)
    rng.shuffle(a)
    return a


def build_plan(total=TOTAL, seed="t60-plan-v1", a10=False):
    a12, a10_ = n_levers(total, a10)
    head_total = util.largest_remainder(total, HEAD_ROWS)
    raw = {}
    for head in M.HEADS:
        main_h = head_total[head] - a12[head] - a10_.get(head, 0)
        names = {k: v[3] for k, v in ENTRIES.items() if v[0] == head}
        raw.update(util.largest_remainder(main_h, names))
    plan = []
    for name, (head, kind, what, _rows) in ENTRIES.items():
        size = GROUP_SIZE[kind]
        n_groups = raw[name] // size
        for i in range(n_groups):
            g = dict(gid="%s-%s-%05d" % (head, name.split("|")[1], i), block=head.upper(), head=head, kind=kind, size=size, entry=name,
                     spec=dict(size=size, name=name))
            if kind == "single":
                g.update(ctl=what, label=LABELS[head][0] if what == "ctl.t60.far_inside" else LABELS[head][1])
            elif head == "h2":
                g.update(h2kind=what)
            else:
                g.update(edit=what)
            plan.append(g)
    # the length-L4 rows are exactly 10% of the clean rows (K15 over-1,024 share <= 10% and K21 length L4 >= 10%): trim the easy control singles so
    # that the number of main rows is a multiple of 10 (at most 9 H1 far-inside singles)
    if total >= 500:
        extra = sum(g["size"] for g in plan) % 10
        fars = {h: [g for g in plan if g["entry"] == h + "|far_inside"] for h in ("h1", "h3")}
        for i in range(extra):
            g = fars["h1" if i % 2 == 0 else "h3"].pop()
            plan.remove(g)
    rng = util.rng_for(seed, "order")
    rng.shuffle(plan)
    # member order (which label comes first), roles, depth for supersession
    for head in M.HEADS:
        gs = [g for g in plan if g["head"] == head and g["kind"] in ("pair", "swap_card")]
        for g, f in zip(gs, _flags(len(gs), 0.5, util.rng_for(seed, "ab", head))):
            g["labels"] = LABELS[head] if f else LABELS[head][::-1]
            g["roles"] = ["a", "b"]
    for g in plan:
        if g["kind"] == "quad":
            g["roles"] = ["a", "b", "c", "d"]
            g["labels"] = None
    sups = [g for g in plan if g.get("h2kind") == "supersede"]               # depth 1 / 2 / 3 = 50 / 30 / 20 (K13, +-5) as an exact share, not one draw per group
    cnt = util.largest_remainder(len(sups), {1: 50, 2: 30, 3: 20})
    seq = [d for d, n in cnt.items() for _ in range(n)]
    util.rng_for(seed, "depth").shuffle(seq)
    for g, d in zip(sups, seq):
        g["depth"] = d
    # world 60 / 40 per head, balanced
    for head in M.HEADS:
        gs = [g for g in plan if g["head"] == head]
        for g, f in zip(gs, _flags(len(gs), P_REPO, util.rng_for(seed, "world", head))):
            g["world"] = "repo" if f else "tool"
            g["view"] = "primary"
    _assign_cards(plan, seed)
    _assign_mentions(plan, seed)
    RC.assign(plan, seed)
    _assign_positions(plan, seed)
    for g in plan:
        g["alarm"] = False
        g.setdefault("labels", None)
    return plan


def _assign_cards(plan, seed):
    cyc = {}
    rng = util.rng_for(seed, "cards")

    def draw(pool, key):
        k = (tuple(pool), key)
        st = cyc.setdefault(k, [[], 0])
        if st[1] >= len(st[0]):
            st[0], st[1] = list(pool), 0
            rng.shuffle(st[0])
        c = st[0][st[1]]
        st[1] += 1
        return c

    for g in plan:
        pool = M.CARDS_BY_HEAD[g["head"]]
        g["card"] = draw(pool, g.get("label") or g.get("edit") or g.get("h2kind") or "x")
        if g.get("h2kind") == "recovery":
            g["card"] = "card.t60.k01"
    _balance_h3_cards(plan)


H3_SWAP_PAIRS = (("card.t60.p01", "card.t60.p03"),) * 4      # the only pair of cards whose n_min differ by 2: the ACT member then sits at pmargin L2 (the easy twin)


def _balance_h3_cards(plan):
    """Skeptic fix (K4 per-card 40-60%, K9 card-only probe). A card-swap pair gives its PLAN member to the card with the smaller n_min and
    its ACT member to the card with the larger n_min, so on its own it ties card p01 to PLAN and card p03 to ACT (measured: p03 PLAN share
    0.37, card-only AUC 0.585). The swap cards are therefore fixed here, at plan level, from a balanced cycle (`card` = the PLAN-side card,
    `card_y` = the ACT-side card), and the single controls (far_inside = PLAN, multi_violation = ACT) take the cards whose running
    PLAN-minus-ACT count is most off, which cancels the swap skew. Pairs and quads give both labels to one card (net zero)."""
    swaps = [g for g in plan if g["head"] == "h3" and g["kind"] == "swap_card"]
    net = {c: 0 for c in M.CARDS_BY_HEAD["h3"]}
    pairs = H3_SWAP_PAIRS
    for i, g in enumerate(swaps):
        x, y = pairs[i % len(pairs)]
        g["card"], g["card_y"] = x, y
        net[x] += 1
        net[y] -= 1
    cards = list(M.CARDS_BY_HEAD["h3"])
    used = {c: 0 for c in cards}                       # ties on the running net go to the card with fewer controls so far (spread)
    for g in plan:
        if g["head"] == "h3" and g["kind"] == "single":
            if g["label"] == "PLAN":
                c = min(cards, key=lambda k: (net[k], used[k], k))
                net[c] += 1
            else:
                c = max(cards, key=lambda k: (net[k], -used[k], k))
                net[c] -= 1
            used[c] += 1
            g["card"] = c


def _assign_mentions(plan, seed):
    """K6 is a share bar on the plan mention of the quoted noun: the decoy flag of the H2 groups is balanced at plan level (exact share), instead of
    one independent draw per group (the 1,000-row shares then do not wander across the bar)."""
    for entry in sorted({g["entry"] for g in plan if g["head"] == "h2"}):
        gs = [g for g in plan if g["entry"] == entry]
        if entry in ("h2|quad", "h2|step_done", "h2|supersede", "h2|pointer"):
            for g, f in zip(gs, _flags(len(gs), B.MENTION_P, util.rng_for(seed, "mention", entry))):
                g["mention"] = f


def _assign_positions(plan, seed):
    rows = []
    for g in plan:
        for i in range(g["size"]):
            lab = g.get("label") if g["kind"] == "single" else (g["labels"][i] if g.get("labels") else "q%d" % i)
            rows.append((g["gid"], i, g["head"], lab))
    by = collections.defaultdict(list)
    for gid, i, head, lab in rows:
        by[(head, lab)].append((gid, i))
    pos = {}
    for key, items in by.items():
        cyc = util.balanced_cycle(len(items), 2, util.rng_for(seed, "pos", *map(str, key)))
        for (gid, i), p in zip(items, cyc):
            pos[(gid, i)] = p
    for g in plan:
        g["pos"] = [pos[(g["gid"], i)] for i in range(g["size"])]


# =============================================================================================================
# generation
# =============================================================================================================
MAX_ATTEMPTS = 12
TOKEN_CAP = 1450


def group_line_problems(recs, g):
    """K10 / K11 at generation: members differ ONLY in line kinds the registered edit may change (a swap: card lines; a quad: markers +
    plan_ref lines) and every pair of members differs at all."""
    probs = []
    if g["kind"] == "quad":
        allowed = {"h2_fact", "h2_quote", "h2_planref"}
        base = collections.Counter(recs[0]["lines"])
        for r in recs[1:]:
            c = collections.Counter(r["lines"])
            diff = (base - c) + (c - base)
            probs += [k for (k, _t), _n in diff.items() if k not in allowed]
        cells = {r["cell"] for r in recs}
        if len(cells) != 4:
            probs.append("cells")
        return sorted(set(probs))
    a, b = collections.Counter(recs[0]["lines"]), collections.Counter(recs[1]["lines"])
    diff = (a - b) + (b - a)
    if not diff:
        return ["members render identically"]
    for (k, _t), _n in diff.items():
        if g["kind"] == "swap_card" or g.get("edit") == "card_swap" or g.get("h2kind") == "recovery":
            if not k.startswith("card_"):
                probs.append(k)
        else:
            owns = M.EDIT_OWNS.get(g.get("edit") or {"pointer": "pointer_content"}.get(g.get("h2kind"), g.get("h2kind")), set())
            if k not in owns:
                probs.append(k)
    return sorted(set(probs))


LEN_BANDS = {1: (0, 499), 2: (510, 790), 3: (840, 960), 4: (1100, 1440)}      # planned tokens by length level; margins keep rewording off 800 / 1,024


def _want_key(g, rec):
    if g["kind"] == "single":
        return "s"
    if g["kind"] == "quad":
        return rec["cell"]
    return rec["gold"]


def _fit_ballast(ctx, g, scenes):
    """Give every member of the group the SAME neutral notes so that all members land in the planned length band (None: no fit)."""
    base, bands = [], []
    for i, s in enumerate(scenes):
        s["ballast"] = []
        r = R.finalize(ctx, g, s, g["pos"][i % g["size"]], i)
        base.append(ballast.n_words(r["rendered"]["text"]))
        key = _want_key(g, r)
        bands.append(g["rc"].get("bands", {}).get(key) or LEN_BANDS[g["rc"]["want"][key]["length"]])      # a member's band follows ITS planned length level
    lines = ballast.choose(util.rng_for(ctx.seed, "ballast", g["gid"]), base, bands)
    if lines is None:
        return False
    for s in scenes:
        s["ballast"] = list(lines)
    return True


def level_mismatch(g, recs):
    """-> list of (key, mechanism, planned, realised) where the realised ladder differs from the plan (Opus ruling Q6, per-row assert)."""
    out = []
    for r in recs:
        key = _want_key(g, r)
        for mech, planned in g["rc"]["want"][key].items():
            if r["levels"][mech] != planned:
                out.append((key, mech, planned, r["levels"][mech]))
    return out


def generate_group(ctx, g):
    last = None
    g = dict(g)
    for attempt in range(MAX_ATTEMPTS):
        g["attempt"] = attempt
        try:
            scenes = B.build_group(ctx, g, attempt)
        except (SceneReject, M.EditNotApplicable, rule_err()) as e:
            last = e
            ctx.rejected = getattr(ctx, "rejected", 0) + 1
            continue
        # per-row check at creation (Opus ruling Q1): a supersede row whose chain repeats a value is dropped here with its own code and
        # counter; it is not a G13 drop, so the same skeleton is regenerated with a new value draw (G0-lite section 7(a))
        if any(B.supersede_row_problems(s) for s in scenes):
            ctx.drops[B.SUPERSEDE_SAME_VALUE] += len(scenes)
            ctx.rejected = getattr(ctx, "rejected", 0) + 1
            last = SceneReject(B.SUPERSEDE_SAME_VALUE)
            continue
        # per-row check at creation (Opus ruling Q6 batch 2, B2-1): no L3 ordinal reference, in any step, lands on a superseded record; a row that breaks it is dropped
        # with its own counter and regenerated on the same skeleton (not a G13 drop). The builder names the current record, so this is the safety net.
        if any(B.ordinal_superseded_problems(s) for s in scenes):
            ctx.drops[B.ORDINAL_ON_SUPERSEDED] += len(scenes)
            ctx.rejected = getattr(ctx, "rejected", 0) + 1
            last = SceneReject(B.ORDINAL_ON_SUPERSEDED)
            continue
        if not _fit_ballast(ctx, g, scenes):
            ctx.drops["length_no_fit"] += len(scenes)
            ctx.rejected = getattr(ctx, "rejected", 0) + 1
            last = SceneReject("length band %d" % g["rc"]["ell"])
            continue
        recs = [R.finalize(ctx, g, s, g["pos"][i % g["size"]], i) for i, s in enumerate(scenes)]
        if any(util.approx_tokens(r["rendered"]["text"]) > TOKEN_CAP for r in recs):
            last = SceneReject("token cap")
            ctx.rejected = getattr(ctx, "rejected", 0) + 1
            continue
        for r in recs:
            r["row_level_target"] = LV.row_level(g["rc"]["want"][_want_key(g, r)])          # the planned row level (manifest metadata, never rendered)
        mism = level_mismatch(g, recs)
        if mism:                                       # planned == realised, else drop (not a G13 drop) and regenerate on the same skeleton
            ctx.drops["level_mismatch"] += len(recs)
            ctx.rejected = getattr(ctx, "rejected", 0) + 1
            last = SceneReject("level mismatch %s" % (mism[:3],))
            continue
        if g["kind"] != "single":
            bad = group_line_problems(recs, g)
            if bad:
                last = SceneReject("group integrity: %s" % bad)
                ctx.rejected = getattr(ctx, "rejected", 0) + 1
                continue
        if g["kind"] == "single":
            want = (g["label"],)
        elif g["kind"] == "quad":
            want = ("KEEP", "DROP", "KEEP", "DROP")
        else:
            want = tuple(g["labels"])
        got = tuple(r["gold"] for r in recs)
        if got != want:
            raise AssertionError("%s: solver A gave %s, the plan intends %s" % (g["gid"], got, want))
        return recs
    raise RuntimeError("group %s rejected %d times: %s" % (g["gid"], MAX_ATTEMPTS, last))


def rule_err():
    import t60_rule
    return t60_rule.SpecError


def generate_in_memory(total=20, seed="t60-dry", standin=True, ctx=None):
    ctx = ctx or Ctx(seed=seed, standin=standin)
    plan = build_plan(total=total, seed=seed)
    recs = []
    for g in plan:
        recs.extend(generate_group(ctx, g))
    return recs
