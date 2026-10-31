"""T67 generator: plan (blocks -> consent groups: single / pair / quad / card-swap) and group generation (spec -> records). No rows are written.

Group kinds (K5 / K8 / K11): single (one row), pair (neither + both naming cells of a soft decision), quad (neither / op / target / both; soft or hard),
swap (the SAME spec under two cards that give different labels; M-2: clause ON vs OFF). Head rows (reason / tier, G7) are derived from KEPT single-trigger
rows of at most 25% of the specs per head and come after the parent rows (`extra_rows`).
"""
import copy

from LP_COMMON import plan as plan_mod
from LP_COMMON import util, wording
from LP_COMMON.plan import Ctx as BaseCtx

from . import builders as B, config as C, engine, rows as ROWS, render as R, sqlmodel as SQ, userturn as UT


def pool_problems(pool):
    """Problems of a T67 wording pool ([] = usable): the shared slot / count / duplicate rules, plus the consent-cell rule for the user turns (GV12 at pool level): a
    turn form that does not name the OPERATION (neither, target) may contain no operation word of the closed lexicon, and the forms that name only one thing carry
    only their own slot (`wording.validate` enforces the slot sets)."""
    import re
    bad = list(wording.validate(pool, UT.FORM_SLOTS))
    for form in ("T67-U-NEITHER", "T67-U-TARGET"):
        for t in wording.texts_of(pool, form):
            for ref, word in UT.OP_WORD.items():
                if re.search(r"(?<![A-Za-z])%s(?![A-Za-z])" % re.escape(word), t):
                    bad.append("%s: wording %r contains the operation word %r (this form must not name the operation)" % (form, t[:50], word))
    return bad


class Ctx(BaseCtx):
    def __init__(self, seed, standin=False, pool_path=None, pool=None, lock_table=None, deny_check=None):
        slots = dict(UT.FORM_SLOTS)
        if pool is None and pool_path is None and standin:
            pool = wording.make_test_pool(slots)
        super().__init__(seed, standin=standin, pool_path=pool_path, pool=pool, deny_check=deny_check)
        if self.pool is None:
            raise wording.PoolError("no wording pool")
        if lock_table is None and standin:
            lock_table = SQ.draft_lock_table()
        if lock_table is None:
            raise ValueError("a lock table is required (T67-B7: the Opus-written, hashed T67-LOCK-TABLE)")
        if not standin:
            wording.require_real(self.pool)
            problems = pool_problems(self.pool)
            if problems:
                raise wording.PoolError("the T67 wording pool is not usable: " + "; ".join(problems[:4]))
            lock_table.require_real()
        self.lock_table = lock_table
        self.picker = wording.Picker(self.pool, util.rng_for("T67-picker", seed))


# ---- plan ------------------------------------------------------------------------------------------------------------------------------
SCN_OF_BLOCK = {"P-a": "destroy", "P-b": "lane", "P-c": "store", "P-d": "benign_plan", "P-e": "key", "K-a": "priv", "K-b": "expose", "K-c": "pvc",
                "K-d": "benign_k8s", "C-a": "pin", "C-b": "trig", "C-c": "prot", "C-d": "benign_ci", "M-1": "m01", "M-2": "m02"}
SWAP_SHARE = 0.06                                 # card-swap rows ~6% of a block (30 specs = 60 rows in the family; M-2 clause swaps are extra)


def allocate(rows, allow, ask, block, name=None):
    """Consent-group counts for a block: (quad_ask, pair_ask, single_ask, quad_block, pair_block, single_block, allow_singles)."""
    def split(n):
        x = int(0.225 * n / 1.0 / 1.0 * 1.0)          # quads and pairs are equally many groups (K5 stratum), together ~90% of the non-ALLOW rows
        x = int(0.9 * n / 4.0)
        y = x
        return x, y, max(0, n - 3 * x - y)
    xa, ya, za = split(ask)
    xb, yb, zb = split(block)
    while allow - (xa + ya + xb + yb) < 0 and (ya + yb) > 0:
        if yb >= ya and yb > 0:
            yb -= 1; zb += 1
        else:
            ya -= 1; za += 1
    a_single = max(0, allow - (xa + ya + xb + yb))
    return xa, ya, za, xb, yb, zb, a_single


def build_plan(total=C.ROWS_TOTAL, seed=0, oversample=True):
    scale = total / float(C.ROWS_TOTAL) * (plan_mod.OVERSAMPLE if oversample else 1.0)
    rng = util.rng_for("T67-plan", seed)
    groups = []
    k = 0

    def add(block, kind, want, n_groups, extra=None):
        nonlocal k
        for _ in range(max(0, n_groups)):
            k += 1
            cell = {"block": block, "scn": SCN_OF_BLOCK[block], "group": kind, "want": want}
            cell.update(extra or {})
            groups.append({"gid": "T67-%s-%04d" % (block, k), "seed": "%s-%d" % (block, k), "size": {"single": 1, "pair": 2, "quad": 4, "swap": 2}[kind],
                           "head": "GATE", "cell": cell})

    for block, b in C.BLOCKS.items():
        allow, ask, blk = [int(round(v * scale)) for v in b["labels"]]
        if block == "M-2":
            # 40 dev rows (ALLOW singles) + 80 unauthorised shared / production rows each with an authorised twin; >= 20 clause swaps
            n_un_ask, n_un_blk = ask, blk
            add(block, "pair", "ASK", n_un_ask)
            add(block, "pair", "BLOCK", n_un_blk)
            add(block, "single", "ALLOW", max(0, allow - n_un_ask - n_un_blk))
            add(block, "swap", "BLOCK", int(round(20 * scale)), {"swap_kind": "clause"})
            continue
        if block in ("P-d", "K-d", "C-d"):
            add(block, "single", "ALLOW", allow)
            continue
        if block == "P-e":
            add(block, "quad", "BLOCK", int(round(5 * scale)), {"hard": True})
            continue
        if block == "P-c":
            hard_q = int(round(5 * scale))
            add(block, "quad", "BLOCK", hard_q, {"hard": True})
            xa, ya, za, xb, yb, zb, a1 = allocate(None, allow, ask, max(0, blk - 4 * hard_q), block)
        else:
            xa, ya, za, xb, yb, zb, a1 = allocate(None, allow, ask, blk, block)
        swaps = int(round(SWAP_SHARE * b["rows"] * scale / 2.0)) if block in ("P-a", "P-b", "K-a", "K-b", "C-a", "C-b", "C-c") else 0
        add(block, "quad", "ASK", xa)
        add(block, "pair", "ASK", ya)
        add(block, "single", "ASK", za)
        add(block, "quad", "BLOCK", xb)
        add(block, "pair", "BLOCK", yb)
        add(block, "single", "BLOCK", zb)
        add(block, "single", "ALLOW", a1)
        add(block, "swap", "BLOCK", swaps, {"swap_kind": "card"})
    rng.shuffle(groups)
    n_held = int(round(C.HELD_OUT_OPERATOR_ROWS * scale / 2.0))                    # dev-only held-out-operator slice, <= 60 rows inside the 1,000
    for g in [g for g in groups if g["size"] == 2 and g["cell"]["group"] == "pair"][:n_held]:
        g["cell"]["heldout_operator"] = True
    levels = plan_mod.level_cycle(len(groups), rng)
    for g, lv in zip(groups, levels):
        g["cell"]["level"] = lv
    # card hints: a balanced cycle per (block, wanted label) so every card sees the same label mix (K8 per-card ALLOW share)
    cyc = {}
    for g in groups:
        c = g["cell"]
        if c["group"] == "swap":
            continue
        key = (c["block"], c["want"])
        pool = [x for x in C.CARD_IDS if C.LEVERS[x]["lock_review"]] if c["block"] == "M-2" else list(C.CARD_IDS)
        if key not in cyc:
            order = list(pool)
            rng.shuffle(order)
            cyc[key] = [order, 0]
        order, i = cyc[key]
        c["card"] = order[i % len(order)]
        cyc[key][1] += 1
    return groups


# ---- generation ------------------------------------------------------------------------------------------------------------------------
def _draw(ctx, g, tag="a", want=None, card_id=None, hard=False):
    R_ = B.Req(ctx, g, tag)
    fn = B.DRAW[g["cell"]["scn"]]
    kw = {"card_id": card_id, "lock": ctx.lock_table}
    if hard and g["cell"]["scn"] == "store":
        kw["hard"] = True
    return R_, fn(R_, want or g["cell"]["want"], **kw)


def generate_group(ctx, g):
    c = g["cell"]
    kind = c["group"]
    last, best = None, None
    want_lv = plan_mod.LEVELS.index(c.get("level", "L2"))
    for t in range(16):
        gg = dict(g, seed="%s#t%d" % (g["seed"], t))
        try:
            if kind == "swap":
                R_, spec, decisive, card_b = _draw_swap(ctx, gg)
            else:
                R_, (spec, decisive) = _draw(ctx, gg, want=c["want"], hard=c.get("hard", False), card_id=(c.get("card") if t < 8 else None))
                card_b = None
        except (B.Reject, engine.Undefined) as e:
            last = e
            continue
        if kind in ("pair", "quad") and not (decisive and (decisive.get("soft") or c.get("hard"))):
            last = B.Reject("no decisive member")
            continue
        spec = B.retune(R_, spec, c.get("level", "L2"), ctx.lock_table)
        d = abs(plan_mod.LEVELS.index(ROWS.spec_level(spec, ctx.lock_table)) - want_lv)
        if best is None or d < best[0]:
            best = (d, R_, spec, decisive, card_b)
        if d == 0:
            break
    if best is None:
        raise last or B.Reject("no spec")
    _d, R_, spec, decisive, card_b = best
    held = c.get("heldout_operator", False)
    R.fill_refs(ctx.rng("refs", g["gid"]), spec)
    style = R.choose_style(ctx.rng("style", g["gid"]), spec, held_out=held)
    if spec["carrier"] == "PLAN_JSON":
        style["module"] = R_.names.get("ns.noun.module", "mod")
    ids = ["a", "b", "c", "d"]
    if kind == "single":
        return [ROWS.build_record(ctx, g, spec, 0, "neither", decisive, style, group_kind="single")]
    if kind == "pair":
        cells = ("neither", "both")
    elif kind == "quad":
        cells = UT.CELLS
    else:
        cells = ("neither", "neither")
    out = []
    for i, cell in enumerate(cells):
        s = spec
        if kind == "swap":
            s = copy.deepcopy(spec)
            if i == 1:
                s["card"] = card_b
        cid = "%s:%s" % (s["block"], "swap" if kind == "swap" else "+".join(engine.evaluate(s, ctx.lock_table).rules))
        out.append(ROWS.build_record(ctx, g, s, i, cell, decisive, style, pair_id=g["gid"], twin_of="%s-%s-g" % (g["gid"], ids[(i + 1) % len(cells)]),
                                     group_kind=kind, construction_id=cid))
    return out


def _draw_swap(ctx, g):
    """The same spec under two cards with different labels: card A draws the spec for the wanted label; card B is another card that changes the label."""
    c = g["cell"]
    pairs = C.CLAUSE_SWAP if c.get("swap_kind") == "clause" else [(a, b) for a in C.CARD_IDS for b in C.CARD_IDS if a < b]
    R0 = B.Req(ctx, g, "swap")
    order = list(pairs)
    R0.rng.shuffle(order)
    for ca, cb in order:
        for flip in (False, True):
            a, b = (cb, ca) if flip else (ca, cb)
            R_ = B.Req(ctx, g, "swap-%s-%s" % (a, b))
            try:
                spec, decisive = B.DRAW[c["scn"]](R_, "BLOCK" if c.get("swap_kind") != "card" else R0.rng.choice(("BLOCK", "ASK")), card_id=a, lock=ctx.lock_table)
            except (B.Reject, engine.Undefined):
                continue
            spec_b = copy.deepcopy(spec)
            spec_b["card"] = _recard(R_, spec, b)
            try:
                la, lb = engine.evaluate(spec, ctx.lock_table).label, engine.evaluate(spec_b, ctx.lock_table).label
            except engine.Undefined:
                continue
            if la != lb:
                return R_, spec, decisive, spec_b["card"]
    raise B.Reject("no swap")


def _recard(R_, spec, card_id):
    """Card `card_id` with the SAME name lists as the spec's card (a swap pair differs only in the lever slots)."""
    new = copy.deepcopy(spec["card"])
    lv = C.LEVERS[card_id]
    new.update(card_id=card_id, ask_on_soft=lv["ask_on_soft"], digest_pin_requirement=lv["digest"], pin_policy=lv["pin_policy"], lock_review=lv["lock_review"],
               display_name=R_.names.get("ns.policy_card", card_id))
    return new
