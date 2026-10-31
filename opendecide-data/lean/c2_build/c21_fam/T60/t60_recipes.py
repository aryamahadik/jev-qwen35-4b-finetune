"""T60 LADDER PLAN (Opus ruling Q6, 18 Oct 2026): a RECIPE for every group, fixed at plan time, before any row is built.
CODE ONLY. `assign(plan, seed)` writes `g["rc"]` on every group:

    rc = dict(ell=<planned length level of every member>,
              spec={member key: <primitive parameters the builder realises>},
              want={member key: {mechanism: planned level}},      # the builder MUST realise exactly these (per-row assert, drop + regenerate)
              hard=<label of the hard member | None>, ...)

member key = the label (pairs, swaps), the quad cell id (quads) or "s" (singles).
Design: one hard member (row level L3-L4) and its easy twin (row level <= L2, same tokens +-15%, same marker count) per pair / quad / swap when the
edit field touches the hard mechanism; mechanisms an edit does not touch are planned at the SAME level on both members; the label of the hard member
alternates across groups; the length-L4 rows (exactly 10% of the family, >= 1,100 tokens) are the control singles, which have no twin by design.
Where the table forces both members hard (an unstated order is `implied by data flow`, L3, on BOTH members of an R1 / R2 / card pair) the plan says so
and the twin rule reports it.
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
import t60_levels as lv  # noqa: E402
import t60_model as M  # noqa: E402

A_LABEL = {"h1": "DELEGATE", "h2": "KEEP", "h3": "PLAN"}
IFF_LEVEL = {"none": 1, "samedir": 2, "explicit": 2, "incoming": 2, "alias": 3, "aliasdiff": 3, "feed": 4, "declout": 4}
FAIL_GAP = {4: 1, 3: 2, 2: 3, 1: 4}                 # steps below S_min for a failing size predicate, by level
P_L2 = 0.40                                         # share of non-carrier groups planned at length L2 (the rest L1)


class Cyc(object):
    """Balanced draws: every option of a key is used equally often (shuffled rounds), so shares do not wander with the seed."""
    def __init__(self, seed):
        self.rng = util.rng_for(seed, "t60-ladder-cyc")
        self.st = {}

    def pick(self, key, options):
        k = (key, tuple(options))
        st = self.st.setdefault(k, [[], 0])
        if st[1] >= len(st[0]):
            st[0] = list(range(len(options)))
            self.rng.shuffle(st[0])
            st[1] = 0
        i = st[0][st[1]]
        st[1] += 1
        return options[i]

    def coin(self, key, p):
        n = 20
        k = int(round(p * n))
        return self.pick(key, [True] * k + [False] * (n - k))


def row_level(w):
    return lv.row_level(w)


# ======================================================================================================================
# H1
# ======================================================================================================================
def _fail_ok(S, level):
    return S - FAIL_GAP[level] >= 1


def _n_for(level, B, side, decor=False):
    """Number of facts the brief needs for a coupling level (None when infeasible)."""
    if side == "pass":
        if level == 1:
            return 0
        if level == 2:
            return 1 if B >= 2 else None
        if level == 3:
            return B
        return B if (B >= 2 and decor) else None
    if level == 3:
        return B + 1
    if level == 4:
        return B + 1 if decor else None
    return B + 2 if level == 2 else B + 3


def _cp_level(n, B, decor):
    if n == 0:
        return 1
    if n < B:
        return 2
    if n in (B, B + 1):
        return 4 if (decor and n >= 2) else 3
    return 2 if n == B + 2 else 1


def _spec(size, bound, needs, iff, card=None, **kw):
    """size = (side, level, route); bound = (side, level); needs = (side, coupling level, derivable); iff = relation form."""
    d = dict(size=size, bound=bound, needs=needs, iff=iff, card=card)
    d.update(kw)
    return d


def _want_of(spec, ell):
    return dict(dmargin=max(spec["size"][1], spec["bound"][1]), coupling=spec["needs"][1], interference=IFF_LEVEL[spec["iff"]], length=ell)


def _baseline(cyc, key, card, cap=2):
    """Untouched baseline levels (<= cap): size pass level, bound pass level, needs pass level."""
    s0 = cyc.pick(key + ".s0", [1, 2][:cap])
    b0 = cyc.pick(key + ".b0", [1, 2][:cap])
    # the untouched coupling of a pair may sit at any level: under the amended twin rule only the DECISIVE mechanism of the hard member has to be <= L2 on its twin
    n0 = cyc.pick(key + ".n0", [1, 1, 2, 3, 4] if card["B_max"] >= 2 else [1, 1, 3])
    return s0, b0, n0


def plan_h1_pair(g, cyc):
    edit = g["edit"]
    cid = g["card"]
    card = M.CARDS[cid]
    S, B = card["S_min"], card["B_max"]
    D, O = "DELEGATE", "DO_HERE"
    route = lambda key: "volume" if cyc.coin(key + ".route", 0.30) else "steps"          # noqa: E731
    members = {}
    if edit == "size_below":
        for _ in range(6):
            hard = cyc.pick("sb.hard", [D, O])
            hl, el = cyc.pick("sb.hl", [3, 4]), cyc.pick("sb.el", [1, 2])
            dl, ol = (hl, el) if hard == D else (el, hl)
            if _fail_ok(S, ol):
                break
            hard = O if hard == D else D
            dl, ol = (hl, el) if hard == D else (el, hl)
            if _fail_ok(S, ol):
                break
            el = 2 if el == 1 else 1
        else:
            raise ValueError("size_below plan infeasible for %s" % cid)
        s0, b0, n0 = _baseline(cyc, "sb", card, cap=min(2, el))
        rt = route("sb")
        members[D] = _spec(("pass", dl, rt), ("pass", b0), ("pass", n0, n0 == 4), "none", cid)
        members[O] = _spec(("fail", ol, "steps"), ("pass", b0), ("pass", n0, n0 == 4), "none", cid)
    elif edit == "coupling":
        hard = cyc.pick("cp.hard", [D, O])
        hl, el = cyc.pick("cp.hl", [3, 4]), cyc.pick("cp.el", [1, 2])
        if hard == D and hl == 4 and B < 2:
            hl = 3
        if hard == O and el == 2 and B < 2:
            el = 1
        s0, b0, _ = _baseline(cyc, "cp", card)
        rt = route("cp")
        if hard == D:
            nd, no = ("pass", hl, hl == 4), ("fail", el, False)
        else:
            nd, no = ("pass", el, False), ("fail", hl, hl == 4)
        members[D] = _spec(("pass", s0, rt), ("pass", b0), nd, "none", cid)
        members[O] = _spec(("pass", s0, rt), ("pass", b0), no, "none", cid)
    elif edit == "result_unbounded":
        hard = cyc.pick("ru.hard", [D, O])
        hl, el = cyc.pick("ru.hl", [3, 4]), cyc.pick("ru.el", [1, 2])
        dl, ol = (hl, el) if hard == D else (el, hl)
        s0, _, n0 = _baseline(cyc, "ru", card, cap=min(2, el))
        rt = route("ru")
        members[D] = _spec(("pass", s0, rt), ("pass", dl), ("pass", n0, n0 == 4), "none", cid)
        members[O] = _spec(("pass", s0, rt), ("fail", ol), ("pass", n0, n0 == 4), "none", cid)
    elif edit in ("shared_write", "pending_dep"):
        s0, b0, n0 = _baseline(cyc, edit, card)
        hard = cyc.pick(edit + ".hard", [D, O])
        if edit == "shared_write":
            if hard == O:
                fo, fd = "alias", cyc.pick("sw.easyD", ["none", "samedir", "samedir"])
            else:
                fd, fo = cyc.pick("sw.hardD", ["aliasdiff", "declout"]), "explicit"
        else:
            if hard == O:
                fo, fd = "feed", cyc.pick("pd.easyD", ["none", "samedir", "samedir"])
            else:
                fd, fo = cyc.pick("pd.hardD", ["aliasdiff", "declout"]), "incoming"
        rt = route(edit)
        members[D] = _spec(("pass", s0, rt), ("pass", b0), ("pass", n0, n0 == 4), fd, cid)
        members[O] = _spec(("pass", s0, rt), ("pass", b0), ("pass", n0, n0 == 4), fo, cid)
    else:
        raise ValueError(edit)
    ell = g["ell"]
    want = {k: _want_of(v, ell) for k, v in members.items()}
    return dict(ell=ell, spec=members, want=want, hard=hard)


# ---- H1 card swaps ------------------------------------------------------------------------------------------------------------------
def _swap_options(bind):
    out = []
    ids = M.CARDS_BY_HEAD["h1"]
    for x in ids:
        for y in ids:
            if x == y:
                continue
            cx, cy = M.CARDS[x], M.CARDS[y]
            if bind == "size":
                for s in range(cx["S_min"], cy["S_min"]):
                    dl = {0: 4, 1: 3, 2: 2}.get(s - cx["S_min"], 1)
                    ol = {1: 4, 2: 3, 3: 2}.get(cy["S_min"] - s, 1)
                    out.append(dict(x=x, y=y, bind="size", steps=s, dl=dl, ol=ol, decor=False))
            elif bind == "brief":
                for n in range(cy["B_max"] + 1, cx["B_max"] + 1):
                    for decor in (False, True):
                        if decor and n < 2:
                            continue
                        dl = _cp_level(n, cx["B_max"], decor)
                        ol = _cp_level(n, cy["B_max"], decor)
                        out.append(dict(x=x, y=y, bind="brief", n=n, dl=dl, ol=ol, decor=decor))
            else:
                for res in range(cy["R_max"] + 1, cx["R_max"] + 1, 10):
                    dd = (cx["R_max"] - res) / float(cx["R_max"])
                    od = (res - cy["R_max"]) / float(cy["R_max"])
                    lvl = lambda d: 4 if d < 0.05 else (3 if d < 0.15 else (2 if d < 0.30 else 1))      # noqa: E731
                    out.append(dict(x=x, y=y, bind="bound", res=res, dl=lvl(dd), ol=lvl(od), decor=False))
    return out


_SWAP_CACHE = {}


def plan_h1_swap(g, cyc):
    binds = ["size", "brief", "brief", "brief", "bound"]
    opts = []
    for _ in range(10):
        bind = cyc.pick("sc.bind", binds)
        if bind not in _SWAP_CACHE:
            _SWAP_CACHE[bind] = _swap_options(bind)
        opts = [o for o in _SWAP_CACHE[bind] if (o["dl"] >= 3) != (o["ol"] >= 3) and (o["dl"] <= 2 or o["ol"] <= 2)]
        if opts:
            break
    if not opts:
        raise ValueError("no H1 swap option")
    hard = cyc.pick("sc.hard", ["DELEGATE", "DO_HERE"])
    pref = [o for o in opts if ((o["dl"] >= 3) == (hard == "DELEGATE"))] or opts
    net = cyc.net                                                 # DELEGATE rows minus DO_HERE rows per card so far: K4 wants 40-60% on every card
    best = min(abs(net[o["x"]] + 1) + abs(net[o["y"]] - 1) for o in pref)
    pref = [o for o in pref if abs(net[o["x"]] + 1) + abs(net[o["y"]] - 1) == best]
    o = pref[int(util.rng_for(g["gid"], "swapopt").random() * len(pref))]
    net[o["x"]] += 1
    net[o["y"]] -= 1
    g["card"] = o["x"]
    hard = "DELEGATE" if o["dl"] >= 3 else "DO_HERE"
    ell = g["ell"]
    shared = dict(bind=o["bind"], decor=o["decor"], steps=o.get("steps"), n=o.get("n"), res=o.get("res"))
    spec, want = {}, {}
    for lab, cid, level in (("DELEGATE", o["x"], o["dl"]), ("DO_HERE", o["y"], o["ol"])):
        spec[lab] = dict(card=cid, shared=shared)
        w = dict(dmargin=1, coupling=1, interference=1, length=ell)
        if o["bind"] in ("size", "bound"):
            w["dmargin"] = level
        else:
            w["coupling"] = level
        want[lab] = w
    return dict(ell=ell, spec=spec, want=want, hard=hard, swap=o)


# ---- H1 controls --------------------------------------------------------------------------------------------------------------------
def plan_h1_single(g, cyc):
    cid = g["card"]
    card = M.CARDS[cid]
    B, S = card["B_max"], card["S_min"]
    ell = g["ell"]
    if g["ctl"] == "ctl.t60.far_inside":
        s0, b0, n0 = _baseline(cyc, "fi", card)
        n0 = min(n0, 2) if card["B_max"] >= 2 else 1                    # far inside: every predicate far from its threshold
        spec = _spec(("pass", s0, "volume" if cyc.coin("fi.route", 0.3) else "steps"), ("pass", b0), ("pass", n0, False), "none", cid)
        return dict(ell=ell, spec={"s": spec}, want={"s": _want_of(spec, ell)}, hard=None)
    # multi_violation: two predicates fail, each near its threshold (L3 / L4); the rest of the row is easy
    pool = ["size", "bound", "brief", "free"]
    k = 4                                                      # every predicate fails (the text asks for two or more), each near its threshold
    skip = None
    picks = [p for p in pool if p != skip]
    spec = _spec(("pass", 1, "steps"), ("pass", 1), ("pass", 1, False), "none", cid)
    hl_dm = cyc.pick("mv.hl.dm", [3, 4])                       # size and bound sit at the same level, so the row's dmargin is that level
    for p in picks:
        hl = hl_dm if p in ("size", "bound") else cyc.pick("mv.hl." + p, [3, 4])
        if p == "size":
            spec["size"] = ("fail", hl if _fail_ok(S, hl) else 3, "steps")
        elif p == "bound":
            spec["bound"] = ("fail", hl)
        elif p == "brief":
            spec["needs"] = ("fail", hl, hl == 4)
        else:
            spec["iff"] = "alias" if hl == 3 else "feed"
    return dict(ell=ell, spec={"s": spec}, want={"s": _want_of(spec, ell)}, hard=None)


# ======================================================================================================================
# H2
# ======================================================================================================================
H2_DIST = [1, 1, 2, 2, 3, 3, 4, 4]                     # planned distance of the KEEP member (steps until the first use: 1, 2-3, 4-7, 8+)
H2_IND = {"quad": [1, 2, 2, 3, 3], "supersede": [1, 2, 3, 3, 3], "step_done": [2, 3, 4, 4, 4, 4], "pointer": [4]}
REC_MODE_QUAD = ["plain"] * 4 + ["k1"] * 2 + ["k2"] * 4          # k1: the star is a counted contingency step (recovery L2); k2: an uncounted one on the DROP cells (L3)
REC_MODE_PAIR = {"supersede": ["plain"] * 5 + ["k1"] * 3 + ["ledger"] * 14, "step_done": ["plain"] * 5 + ["k1"] * 3 + ["ledger"] * 14,
                 "pointer": ["plain"] * 4 + ["k1"] * 1}


def h2_want(m, dist, ind, ell, kind, mode=None):
    """Planned levels of the KEEP and DROP members of a pair (relative semantics, t60_levels). mode k1: the star is a counted contingency step (recovery L2
    on both members; a host step stands before it, so the first use is at least the second step). mode ledger: the same with a ledger key (state key read
    only by the counted read-back step, a persisted copy as decoy): recovery L4 on the KEEP member."""
    r = 2 if mode in ("k1", "ledger") else 1
    keep = dict(salience=4 - m, distance=dist, indirection=ind, recovery=4 if mode == "ledger" else r, length=ell)
    drop = dict(salience=1 + m, distance=1, indirection=1, recovery=r, length=ell)
    if kind == "recovery":
        keep.update(distance=2, indirection=2 if mode == "ledger" else 1, recovery=4 if mode == "ledger" else 2)
        drop.update(recovery=3)
    return {"KEEP": keep, "DROP": drop}


def plan_h2(g, cyc):
    kind = g["h2kind"]
    ell = g["ell"]
    if kind == "quad":
        mode = cyc.pick("q.mode", REC_MODE_QUAD)
        ind = cyc.pick("q.ind", H2_IND["quad"])
        dist = cyc.pick("q.dist", [1, 1, 2, 2, 3] if mode == "plain" else [2, 2, 3])
        g["card"] = {"k1": "card.t60.k01", "k2": "card.t60.k02"}.get(mode, g["card"])
        ra, rb = {"plain": (1, 1), "k1": (2, 2), "k2": (1, 3)}[mode]            # recovery of the needed cells / of the unneeded cells
        want = {
            M.QUAD_CELLS[(True, True)]: dict(salience=1, distance=dist, indirection=ind, recovery=ra, length=ell),
            M.QUAD_CELLS[(True, False)]: dict(salience=4, distance=1, indirection=1, recovery=rb, length=ell),
            M.QUAD_CELLS[(False, True)]: dict(salience=4, distance=dist, indirection=ind, recovery=ra, length=ell),
            M.QUAD_CELLS[(False, False)]: dict(salience=1, distance=1, indirection=1, recovery=rb, length=ell),
        }
        return dict(ell=ell, spec={}, want=want, hard=None, dist=dist, ind=ind, m=None, kind=kind, mode=mode)
    m = cyc.pick(kind + ".m", [0, 1, 2, 3])                      # m and 3 - m equally often inside every pair kind
    if kind == "recovery":
        return dict(ell=ell, spec={}, want=h2_want(m, 2, 1, ell, kind), hard=None, dist=2, ind=1, m=m, kind=kind, mode=None)
    mode = cyc.pick(kind + ".mode", REC_MODE_PAIR[kind])
    ind = 2 if mode == "ledger" else cyc.pick(kind + ".ind", H2_IND[kind])           # a ledger key is taken by role description (L2)
    deep = kind == "supersede" and g.get("depth", 1) >= 2                              # supersession depth >= 2 is indirection L4 (section 5 table)
    eff_ind = 4 if deep else ind
    # the high levels of the KEEP member are stacked on the same rows (fewer L4 rows for the same fill): a ledger key sits far from its first use (L4),
    # a pointer / deep chain at L3, the rest stays near
    if mode == "ledger":
        dist = 4
    elif mode == "k1":
        dist = cyc.pick(kind + ".distk1", [2, 3, 4, 4])
    else:
        dist = 3 if eff_ind == 4 else cyc.pick(kind + ".dist", [1, 1, 2, 2])
    if mode in ("k1", "ledger"):
        g["card"] = "card.t60.k01"
    want = h2_want(m, dist, ind, ell, kind, mode)
    if kind == "supersede" and g.get("depth", 1) >= 2:
        want["KEEP"]["indirection"] = 4                           # supersession depth >= 2 is indirection L4 (section 5 table)
    return dict(ell=ell, spec={}, want=want, hard=None, dist=dist, ind=ind, m=m, kind=kind, mode=mode)


# ======================================================================================================================
# H3
# ======================================================================================================================
def _irrev_level(form):
    return {"plain": 1, "magn": 3, "ext": 3, "expired": 4, "undo_long": 1, "undo_short": 2}[form]


def _h3_want(spec, ell, repo=False, edit=None):
    card = M.CARDS[spec["card"]]
    d = abs(spec["n"] - card["n_min"])
    o = spec["order"][0]
    dv = (4 if spec.get("derived") else 3) if o == "unstated" else (2 if o == "numbered" else 1)
    irr = _irrev_level(spec["irrev"])
    if repo and spec["irrev"] in ("ext", "expired", "undo_short"):
        raise ValueError("form %s needs a tool-world undo window" % spec["irrev"])
    return dict(pmargin={0: 4, 1: 3, 2: 2}.get(d, 1), irrev=irr, depvis=dv, length=ell)


SHARED_FORMS_TOOL = ("plain",) * 3 + ("magn",) * 1 + ("ext",) * 2 + ("expired",) * 5         # irrev L1 / L3 / L3 / L4 on the untouched mechanism of a pair
SHARED_FORMS_REPO = ("plain",) * 7 + ("magn",) * 3
SHARED_FORMS_SW_TOOL = ("plain",) * 1 + ("magn",) * 1 + ("ext",) * 1 + ("expired",) * 7              # card swaps: the shared form is hard on both members
SHARED_FORMS_SW_REPO = ("plain",) * 1 + ("magn",) * 5
UA_K = [0, 2, 2, 3]                                                       # undo_added: steps above n_min (0 = pmargin L4 on both members)
SW_D = [3, 3, 4]                                                          # card swaps: visibility of the unstated order (3 data flow, 4 derived value)


def _forms_r1(world, cyc, key, weights=None):
    if weights is None:
        weights = SHARED_FORMS_TOOL if world == "tool" else SHARED_FORMS_REPO
    pool = list(weights) if world == "tool" else [f for f in weights if f in ("plain", "magn")]
    return cyc.pick(key, pool)


def _h3_ell(rc_ell, spec):
    return {k: rc_ell for k in spec}


def plan_h3_pair(g, cyc):
    edit = g["edit"]
    card = M.CARDS[g["card"]]
    n_min = card["n_min"]
    world = g["world"]
    ell = g["ell"]
    P, A = "PLAN", "ACT"
    d_unst = cyc.pick(edit + ".d", [3, 3, 4])                   # visibility of the unstated order (L3 data flow, L4 derived value)
    derived = d_unst == 4                                       # a property of the DATA FLOW: both members show the same flow lines
    spec, hard, ells, bands = {}, None, None, None
    cid = g["card"]
    if edit == "undo_added":
        f_p = _forms_r1(world, cyc, "ua.form", ("plain",) * 4 + ("magn", "ext") if world == "tool" else None)
        f_a = "undo_short" if world == "tool" else "undo_long"
        n = n_min + cyc.pick("ua.k", UA_K)
        spec[P] = dict(n=n, irrev=f_p, order=("unstated",), derived=derived, card=cid)
        spec[A] = dict(n=n, irrev=f_a, order=("unstated",), derived=derived, card=cid)
        hard = P
    elif edit == "step_count":
        # hard PLAN at n_min (pmargin L4), easy ACT two steps below (pmargin L2). The members differ by two steps (110-140 tokens), so the +-15% twin needs
        # rows of 1,100+ tokens: both members are length L4 (label-balanced L4 rows that have a twin). Cards with n_min >= 4 only (ACT needs >= 2 steps).
        cid = g["card"] = cyc.pick("sc.card", ["card.t60.p02", "card.t60.p03", "card.t60.p04"])
        n_min = M.CARDS[cid]["n_min"]
        f = _forms_r1(world, cyc, "sc.form")
        n_p, n_a, hard = n_min, n_min - 2, P
        ells = {P: 4, A: 4}
        bands = {A: (1100, 1180), P: (1160, 1320)}
        spec[P] = dict(n=n_p, irrev=f, order=("unstated",), derived=derived, card=cid)
        spec[A] = dict(n=n_a, irrev=f, order=("unstated",), derived=derived, card=cid)
    elif edit == "order_stated":
        n = n_min + cyc.pick("os.k", [2, 3])
        stated = cyc.pick("os.stated", ["words", "numbered"])
        f = _forms_r1(world, cyc, "os.form", ("plain",) * 6 + ("magn", "ext"))
        spec[P] = dict(n=n, irrev=f, order=("unstated",), derived=derived, card=cid)
        spec[A] = dict(n=n, irrev=f, order=(stated,), derived=derived, card=cid)
        hard = P
    else:
        raise ValueError(edit)
    ells = ells or _h3_ell(ell, spec)
    want = {lab: _h3_want(sp, ells[lab], edit=edit) for lab, sp in spec.items()}
    rc = dict(ell=max(ells.values()), spec=spec, want=want, hard=hard)
    if bands:
        rc["bands"] = bands
    return rc


def plan_h3_swap(g, cyc):
    x = g["card"]
    y = g.get("card_y") or x
    ell = g["ell"]
    world = g["world"]
    f = _forms_r1(world, cyc, "h3sw.form", SHARED_FORMS_SW_TOOL if world == "tool" else SHARED_FORMS_SW_REPO)       # the form is shared by both members, so the ACT member (pmargin L2) is
    d_unst = cyc.pick("h3sw.d", SW_D)                      # L4 too when the window expires (irrev 4) or the order is a derived value (depvis 4): hard members of both labels
    n = M.CARDS[x]["n_min"]                                     # PLAN at n_min of the smaller card (pmargin L4); under the larger card the ACT member is two steps
    spec = {"PLAN": dict(n=n, irrev=f, order=("unstated",), derived=d_unst == 4, card=x),         # below n_min (pmargin L2: the easy twin)
            "ACT": dict(n=n, irrev=f, order=("unstated",), derived=d_unst == 4, card=y)}
    return dict(ell=ell, spec=spec, want={k: _h3_want(v, ell, edit="card_swap") for k, v in spec.items()}, hard="PLAN")


def plan_h3_single(g, cyc):
    cid = g["card"]
    card = M.CARDS[cid]
    n_min = card["n_min"]
    ell = g["ell"]
    world = g["world"]
    if g["ctl"] == "ctl.t60.far_inside":                         # PLAN with all three predicates far inside
        spec = dict(n=n_min + cyc.pick("h3fi.k", [2, 3]), irrev=_forms_r1(world, cyc, "h3fi.form", ("plain", "magn", "ext")),
                    order=("unstated",), derived=False, card=cid)
    else:                                                        # ACT with none of the three: few steps, undoable, every dependency stated
        spec = dict(n=max(2, n_min - 1), irrev="undo_short" if world == "tool" else "undo_long",
                    order=(cyc.pick("h3mv.stated", ["words", "numbered"]),), derived=False, card=cid)
    return dict(ell=ell, spec={"s": spec}, want={"s": _h3_want(spec, ell)}, hard=None)


# ======================================================================================================================
P_H2_PAIR_L3 = 0.45                                # share of the other H2 pair groups planned at length L3 (KEEP rows are hard, so few easy rows remain; K4 at L2)
P_L3 = 0.115                                       # share of the main rows planned at length L3 (fill >= 10%; 800-1,024 tokens)


def assign_length(plan, seed):
    """Length level of every group. Length L4 is exactly 10% of the main rows: the control singles carry it (half per head, H3 half PLAN / half ACT, so the
    notes do not tell the label) together with the step-count pairs on the smallest card, whose three-step difference needs long rows for the +-15% twin.
    Length L3 (P_L3 of the rows) goes to pair / quad / swap groups at random; the step-count pairs on the larger cards put their PLAN member there."""
    n_rows = sum(g["size"] for g in plan)
    n4 = int(round(0.10 * n_rows))                     # a multiple of 10 rows (t60_generator.build_plan): exactly 10%
    sc3 = [g for g in plan if g.get("edit") == "step_count"]
    sc_big = []
    rest = n4 - 2 * len(sc3)
    ctl = lambda h, c: [g for g in plan if g["head"] == h and g.get("ctl") == c]                                       # noqa: E731
    quota = {"h1": rest - rest // 2, "h3": rest // 2}
    h1_mv, h1_far = ctl("h1", "ctl.t60.multi_violation"), ctl("h1", "ctl.t60.far_inside")
    nf = quota["h1"] // 2                                         # half far-inside (label DELEGATE: L3 rows by length alone), half multi-violation (DO_HERE: L4 anyway), so the long rows
    take = h1_far[:nf]                                            # of H1 do not tell the label (single-feature tokens AUC 0.57 -> 0.50 when all carriers were DELEGATE)
    take += h1_mv[:quota["h1"] - len(take)]
    take += h1_far[nf:nf + max(0, quota["h1"] - len(take))]
    h3_far, h3_mv = ctl("h3", "ctl.t60.far_inside"), ctl("h3", "ctl.t60.multi_violation")
    take += h3_mv[:quota["h3"]]
    take += h3_far[:quota["h3"] - len(h3_mv[:quota["h3"]])]
    chosen = {g["gid"] for g in take}
    rng = util.rng_for(seed, "t60-ell")
    pool = [g for g in plan if g["gid"] not in chosen and g["kind"] != "single" and g not in sc3 and g not in sc_big]
    rng.shuffle(pool)
    pool.sort(key=lambda g: 0 if g["kind"] == "quad" else 1)      # quads first: their DROP and KEEP hard cells then reach L4 together (label-balanced L4 rows)
    l3, need = set(), int(round(P_L3 * n_rows)) - len(sc_big)
    for g in pool:
        if need <= 0 and g["kind"] != "quad":
            break
        l3.add(g["gid"])                                          # every quad is length L3: its hard cells (DROP sal 4 / KEEP sal 4) are then L4 together
        need -= g["size"]
    for g in plan:
        if g["gid"] in chosen:
            g["ell"] = 4
        elif g["gid"] in l3:
            g["ell"] = 3
        else:
            g["ell"] = 2 if rng.random() < P_L2 else 1
    return n4 - len(chosen) - 2 * len(sc3)


def est_base_tokens(g, rc):
    """Rough token count of the group's rows before the notes (calibrated on dry-run medians); a group above 440 cannot be planned at length L1."""
    head = g["head"]
    if head == "h1":
        steps = []
        for sp in rc["spec"].values():
            if "size" in sp:
                c = M.CARDS[sp["card"]]
                side, level, route = sp["size"]
                if side == "pass" and route == "steps":
                    steps.append(c["S_min"] + ({4: 0, 3: 1, 2: 2}.get(level, 3)))
                elif side == "fail":
                    steps.append(c["S_min"] - FAIL_GAP[level])
                else:
                    steps.append(c["S_min"] - 1)
            else:
                steps.append(max(M.CARDS[x]["S_min"] for x in M.CARDS_BY_HEAD["h1"]) + 3 if rc.get("swap", {}).get("bind") != "size" else rc["swap"]["steps"])
        extra = 40 if any(sp.get("iff", "none") != "none" for sp in rc["spec"].values()) else 0         # a longer pending line / one more file line
        if g.get("ctl") == "ctl.t60.multi_violation":
            extra += 90                                                                                 # four failing predicates: all facts needed, a fed file, a pending feed
        return 345 + 12 * max(steps + [3]) - 40 + extra
    if head == "h2":
        pads = {1: 0, 2: 1.5, 3: 4.5, 4: 8}[rc["dist"]]
        return 330 + 14 * pads + (35 if g["h2kind"] in ("pointer", "supersede") else 0) + 22 * g.get("depth", 0)
    n = max(sp["n"] for sp in rc["spec"].values())
    words = any(sp["order"][0] == "words" for sp in rc["spec"].values())
    special = any(sp["irrev"] in ("ext", "expired", "undo_short") for sp in rc["spec"].values())
    base = (175 + 56 * n) if g["world"] == "repo" else (150 + 48 * n)
    return base + (12 * (n - 1) if words else 0) + (25 if any(sp["order"][0] == "unstated" and sp.get("derived") for sp in rc["spec"].values()) else 0) + (25 if special else 0)


def _plan_one(g, cyc):
    head = g["head"]
    if head == "h1":
        if g["kind"] == "single":
            return plan_h1_single(g, cyc)
        return plan_h1_swap(g, cyc) if g["kind"] == "swap_card" else plan_h1_pair(g, cyc)
    if head == "h2":
        return plan_h2(g, cyc)
    if g["kind"] == "single":
        return plan_h3_single(g, cyc)
    return plan_h3_swap(g, cyc) if g["kind"] == "swap_card" else plan_h3_pair(g, cyc)


def assign(plan, seed):
    assign_length(plan, seed)
    cyc = Cyc(seed)
    cyc.net = collections.Counter()
    for g in plan:                                                # the single controls fix part of every H1 card's label balance before the swaps are chosen
        if g["head"] == "h1" and g["kind"] == "single":
            cyc.net[g["card"]] += 1 if g["ctl"] == "ctl.t60.far_inside" else -1
    for g in plan:
        g["rc"] = rc = _plan_one(g, cyc)
        if g["head"] == "h2" and g["h2kind"] in ("pointer", "supersede", "step_done") and g["ell"] < 3 and (rc["m"] == 3 or cyc.coin("h2.ell3", P_H2_PAIR_L3)):
            g["ell"] = 3                                          # salience 4 on the DROP member + length L3: a DROP row at L4 (balances the KEEP rows at L4)
            rc["ell"] = 3
            for w in rc["want"].values():
                w["length"] = 3
        if g["ell"] == 1 and g.get("edit") != "step_count" and est_base_tokens(g, rc) > 390:                                     # estimates are for the seed pool; the production pool adds ~35       # no room for a length-L1 row (< 500 tokens): plan it at L2 (same recipe, only the length moves)
            g["ell"] = 2
            rc["ell"] = 2
            for w in rc["want"].values():
                w["length"] = 2
    return plan


def planned_rows(plan):
    """[(head, label, row level, gid, key)] from the plan alone (for design checks)."""
    out = []
    for g in plan:
        for k, w in g["rc"]["want"].items():
            out.append((g["head"], k, row_level(w), g["gid"], g.get("kind")))
    return out
