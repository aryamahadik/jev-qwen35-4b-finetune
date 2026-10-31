"""F5 base generation: slot plans per antithetic card pair, structures meeting the slot targets (label-first by
rejection), contrast pairs (one input change flips every A, N, D, V gold), then A / N / D / V / V' questions.

Phase 1 (structures): per slot, sample M until v(P) equals the target and a V core of the planned family and C2 count
has the target gold. Phase 2 (questions): A / N / D framing drawn at the V framed share of the sampler (framed share
equal per row type, SEM-01), N and D from exact contradictory compositions only (section 4), D from two L_core cues on
>= 15% of bases (k_syn quota, SC8).
"""
from __future__ import annotations

import copy

from . import forms
from .common import rng_for, uhash
from .forms import FRAMES, TAILS, compose

V_K_WEIGHTS = [0.10, 0.40, 0.30, 0.20]
FRAME_IDS = sorted(FRAMES)
ND_FAMS = {"C1", "C3", "C5", "C6", "C8", "C13"}
TRUTH_FUNCTIONAL = {"C1", "C2", "C3", "C5", "C6"}


class SlotFail(Exception):
    pass


def hooks_for(sampler):
    import importlib
    return importlib.import_module(f".{sampler.lower()}_hooks", __package__)


def H_for(card):
    """Hooks for a card: inverted cards (S1 / S4) use the inverted-card sub-sampler."""
    if card.get("inverted"):
        from . import sinv_hooks
        return sinv_hooks
    return hooks_for(card["sampler"])


# ---------------------------------------------------------------------------------------------------------------------
# slot plans

def plan_slots(ca, n, rng, *, probe=False):
    """Slots for card ca; its antithetic partner gets the mirrored targets (v -> 1-v, g -> 1-g)."""
    H = H_for(ca)
    a = ca["a_card"]
    p = ca["p_card"]
    n_pairs = int(round(p * n / 2))
    n_pair_bases = 2 * n_pairs
    nu = n - n_pair_bases
    ones_v = int(round(a * n)) - n_pairs
    ones_g = int(round(a * n)) - n_pairs
    ones_v = max(0, min(nu, ones_v))
    ones_g = max(0, min(nu, ones_g))
    vs = [1] * ones_v + [0] * (nu - ones_v)
    gs = [1] * ones_g + [0] * (nu - ones_g)
    rng.shuffle(vs)
    rng.shuffle(gs)
    slots = []
    for j in range(n_pairs):
        v, g = rng.randrange(2), rng.randrange(2)
        slots.append({"pair": j, "role": "B", "v": v, "g": g})
        slots.append({"pair": j, "role": "Bp", "v": 1 - v, "g": 1 - g})
    for v, g in zip(vs, gs):
        slots.append({"pair": None, "role": None, "v": v, "g": g})
    n_att = int(round(ca["f_card"] * n))
    att = [True] * n_att + [False] * (n - n_att)
    rng.shuffle(att)
    for i, s in enumerate(slots):
        s["i"] = i
        s["attack"] = att[i]
        s["tag"] = "bad" if i % 2 else "good"
        s["vk"] = rng.choices(range(4), V_K_WEIGHTS)[0]
        s["two_lcore"] = rng.random() < 0.18
        if hasattr(H, "T_BUCKETS"):        # text-side cue count target, mirrored, so P(yes | t_txt) is balanced
            s["tb"] = rng.choices(list(H.T_BUCKETS), list(H.T_BUCKETS.values()))[0]
        s.update(H.plan_slot(ca, rng, s))
    # pair members share the template choices of B
    by_pair = {}
    for s in slots:
        if s["pair"] is not None:
            by_pair.setdefault(s["pair"], []).append(s)
    for j, (b, bp) in by_pair.items():
        for k in ("vk", "two_lcore", "tag", "depth", "kind", "which", "bkind", "tb"):
            if k in b:
                bp[k] = b[k]
    return slots


def mirror(slots):
    out = []
    for s in slots:
        t = dict(s)
        t["v"], t["g"] = 1 - s["v"], 1 - s["g"]
        out.append(t)
    return out


# ---------------------------------------------------------------------------------------------------------------------
# phase 1: one base

def usable(c, pos):
    """A core may take a position unless the probe hold-out holds that template (training rows only)."""
    from . import bank
    if pos == "m" and not c.matrix:
        return False
    return not bank.core_held(c, pos)


def c2_ok(which):
    from . import bank
    return not bank.c2_held(which)


def v_choices(H, card, M, P, cores_, k, g, need_pfun):
    """V realizations of total k with gold g: (core, nC2) where the core is a V cue for this sampler."""
    vcores = [c for c in cores_.values() if H.is_v_core(card, c) and (usable(c, "e") or usable(c, "m"))]
    out = []
    lfs = []
    cand = []
    for c in vcores:
        n2 = k - c.k
        if n2 < 0 or n2 > 2:
            continue
        if c.k == 0 and n2 > 0:
            continue                      # a k = 0 V form takes no C2 on top (its counted cue would be C2)
        if n2 > 0 and not usable(c, "e"):
            continue
        if need_pfun and c.rel == "other":
            continue
        lf = c.lf
        for _ in range(n2):
            lf = ["not", lf]
        cand.append((c, n2))
        lfs.append(lf)
    if not cand:
        return []
    try:
        vals = H.solve(M, lfs)
    except Exception:
        # evaluate one by one (some LFs may be undetermined on open cards)
        vals = []
        for lf in lfs:
            try:
                vals.append(H.solve(M, [lf])[0])
            except Exception:
                vals.append(None)
    for (c, n2), val in zip(cand, vals):
        if val is not None and (g is None or int(val) == g):
            out.append((c, n2, int(val)))
    return out


def vcls(c):
    """V template class: the core id without its pack words (with the slot's vk it fixes the V template key)."""
    return c.tid.split(":")[0]


def build_base(card, slot, rng, *, attempts=160, pair_slot=None, force_cls=None, exclude_cls=()):
    """force_cls / exclude_cls (repair r2): an unpaired slot and its mirrored slot in the partner card use the same
    V template class, so every V template is seen with gold g and 1 - g (per-template balance by construction)."""
    H = H_for(card)
    for _ in range(attempts):
        ctx = dict(card)
        ctx.update(H.slot_ctx(card, slot, rng))
        r = H.build_structure(ctx, slot, rng)
        if r is None:
            continue
        M, P, info = r
        if slot.get("tb") and hasattr(H, "t_bucket") and pair_slot is None and slot["pair"] is None \
                and H.t_bucket(M) != slot["tb"]:
            continue
        try:
            (v,) = H.solve(M, [P])
        except Exception:
            continue
        if int(v) != slot["v"]:
            continue
        cores_ = H.cores(ctx, M, P, rng, slot)
        # a contrast pair holds one Yes and one No V gold whatever B's V gold is, so a pair slot leaves g free
        ch = v_choices(H, ctx, M, P, cores_, slot["vk"], None if pair_slot is not None else slot["g"],
                       need_pfun=slot["pair"] is not None)
        if force_cls is not None:
            ch = [x for x in ch if vcls(x[0]) == force_cls]
        elif exclude_cls:
            ch = [x for x in ch if vcls(x[0]) not in exclude_cls]
        if not ch:
            continue
        rng.shuffle(ch)
        for c, n2, gv in ch[:4]:
            sl = dict(slot, g=gv) if pair_slot is not None else slot
            b = {"card": card, "ctx": ctx, "slot": sl, "M": M, "P": P, "info": info, "cores": cores_, "v": int(v),
                 "vcore": c.tid, "vn2": n2}
            if pair_slot is None:
                return b
            nb = pair_base(card, b, dict(pair_slot, g=1 - gv), rng)   # only a B that has a B'
            if nb is not None:
                nb["slot"] = dict(pair_slot, g=1 - gv)
                b["_pair"] = nb
                return b
    raise SlotFail(f"{card['card_id']} slot {slot['i']}")


def pair_base(card, base, slot, rng):
    """B' from B by one input change (closed list per sampler) that flips v(P) and the gold of every A, N, D, V row."""
    H = H_for(card)
    c = base["cores"][base["vcore"]]
    vlf = c.lf
    for _ in range(base["vn2"]):
        vlf = ["not", vlf]
    for desc, M2 in H.perturb(base["M"], rng)[:60]:
        try:
            (v2, g2) = H.solve(M2, [base["P"], vlf])
        except Exception:
            continue
        if int(v2) == 1 - base["v"] and int(g2) == 1 - slot_g(base):
            if not H.valid_structure(base["ctx"], M2, base["P"]):
                continue
            nb = dict(base)
            nb["M"] = M2
            nb["v"] = int(v2)
            nb["pair_change"] = desc
            nb["slot"] = slot
            nb["cores"] = H.cores(base["ctx"], M2, base["P"], rng_for("pair-cores", desc), slot)
            if base["vcore"] not in nb["cores"]:
                continue
            return nb
    return None


def slot_g(base):
    return base["slot"]["g"]


# ---------------------------------------------------------------------------------------------------------------------
# phase 2: questions

def row_lfs(base):
    return base["rows"]


def pick_frame(*key):
    return FRAME_IDS[int(uhash(*key) * len(FRAME_IDS))]


def compose_v(base, q_v, rng):
    """The V question first (its framing share then sets the A / N / D framing share, SEM-01 equal shares)."""
    card, cores_ = base["card"], base["cores"]
    bid = base.get("mk", base["base_id"])   # repair r2: mirrored slots share every question-side draw
    pre_ok = [p for p in ("C2n", "C2f") if c2_ok(p)]
    c2m_ok = c2_ok("C2m")

    def framed(tag):
        return uhash("frame", bid, tag) < q_v

    def tail(tag):
        return TAILS[int(uhash("tail", bid, tag) * len(TAILS))]
    rows = {}
    vc = cores_[base["vcore"]]
    n2 = base["vn2"]
    ue, um = usable(vc, "e"), usable(vc, "m")
    if n2 == 0:
        fr = (framed("V") and ue) or not um
        rows["V"] = compose(vc, pick_frame(bid, "V"), ()) if fr else compose(vc, "mq", (), tail("V"))
    else:
        if not ue:
            raise SlotFail("V core only usable as a matrix question but needs an embedding")
        fr = framed("V") or not c2m_ok
        pre = tuple(rng.choice(pre_ok) for _ in range(n2 - (0 if fr else 1)))
        rows["V"] = compose(vc, pick_frame(bid, "V") if fr else "C2m", pre, "" if fr else tail("V"))
    base["vrow"] = rows["V"]
    return rows["V"]


def compose_rows(base, s_frame, rng):
    """A, N, D, V (and V') question specs for one base. Probe hold-out templates are never used (bank.held)."""
    card, slot, cores_ = base["card"], base["slot"], base["cores"]
    H = H_for(card)
    bid = base.get("mk", base["base_id"])   # repair r2: mirrored slots share every question-side draw
    P = base["P"]
    pre_ok = [p for p in ("C2n", "C2f") if c2_ok(p)]
    c2m_ok = c2_ok("C2m")
    idc = [c for c in cores_.values() if c.k == 0 and not c.fam and c.lf == P]
    vfam = set(cores_[base["vcore"]].fam) - {"C1", "C2"}   # V's counted cue is never N's or D's composition
    nd1 = [c for c in cores_.values() if c.nd and c.k == 1 and set(c.fam) <= ND_FAMS and H.nd_ok(card, c)
           and not (set(c.fam) & vfam)]
    nd2 = [c for c in cores_.values() if c.nd and c.k == 2 and set(c.fam) <= ND_FAMS and H.nd_ok(card, c)
           and not (set(c.fam) & vfam)]
    c1 = [c for c in nd1 if c.fam == ("C1",) and usable(c, "e")]
    rows = {}

    def framed(tag):
        return uhash("frame", bid, tag) < s_frame

    def tail(tag):
        return TAILS[int(uhash("tail", bid, tag) * len(TAILS))]

    def pre1():
        return (rng.choice(pre_ok),)
    # A
    fr = framed("A")
    m_opts = [c for c in idc if usable(c, "m")]
    e_opts = [c for c in idc if usable(c, "e")]
    if (fr and e_opts) or not m_opts:
        rows["A"] = compose(rng.choice(e_opts), pick_frame(bid, "A"))
    else:
        rows["A"] = compose(rng.choice(m_opts), "mq", (), tail("A"))
    # N
    fr = framed("N")
    opts = []
    if fr:
        opts += [(c, pick_frame(bid, "N"), ()) for c in nd1 if usable(c, "e")]
        opts += [(c, pick_frame(bid, "N"), pre1()) for c in e_opts]
    else:
        opts += [(c, "mq", ()) for c in nd1 if usable(c, "m")]
        if c2m_ok:
            opts += [(c, "C2m", ()) for c in e_opts]
    if not opts:
        opts = [(c, pick_frame(bid, "N"), pre1()) for c in e_opts]
    c, outer, pre = rng.choice(opts)
    rows["N"] = compose(c, outer, pre, tail("N") if outer in ("mq", "C2m") else "")
    # D: two-L_core D rows are always framed, so the other D rows use p_D = (s - 0.16) / 0.84 (equal shares)
    fr = uhash("frame", bid, "D") < max(0.0, (s_frame - 0.16) / 0.84)
    if slot.get("two_lcore") and c1 and c2_ok("C2n"):  # forced framed; the other D rows use p_D below
        c = rng.choice(c1)
        rows["D"] = compose(c, pick_frame(bid, "D"), ("C2n",))
        base["two_lcore"] = True
    else:
        opts = []
        if fr:
            opts += [(c, pick_frame(bid, "D"), ()) for c in nd2 if usable(c, "e")]
            opts += [(c, pick_frame(bid, "D"), pre1()) for c in nd1 if usable(c, "e")]
        elif c2m_ok:
            opts += [(c, "C2m", ()) for c in nd1 if usable(c, "e")]
            opts += [(c, "C2m", pre1()) for c in e_opts]
        if not opts:
            opts = [(c, pick_frame(bid, "D"), (pre_ok[0], pre_ok[0])) for c in e_opts] if (fr or not c2m_ok) else \
                [(c, "C2m", (pre_ok[0],)) for c in e_opts]
        c, outer, pre = rng.choice(opts)
        rows["D"] = compose(c, outer, pre, tail("D") if outer == "C2m" else "")
        base["two_lcore"] = False
    rows["V"] = base["vrow"]
    if slot["attack"]:
        rows["Vp"] = rows["V"]
    return rows


def recompose_like(base_b, base_p):
    """B' uses B's question templates: the same cores, outers, prefixes and tails, re-evaluated on M'."""
    return base_b["rows"]
