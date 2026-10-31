"""Spec planner: quotas, pair groups, facts-absent stratum, held-out draw. Produces SPECS only (no text, no rows).

Shares (G0-lite section 3, as fractions of N): ALLOW 15% (clean twin 9, noise 6); ALLOW_BENIGN 35% (delegated 14,
ambient 12, trigger/security 5, human/off-topic 4); BLOCK 35% (unrequested HIGH 20, unrequested LOW 6, HARD
delegated-or-necessary 9); ASK 15% (delegated SOFT 5, necessary SOFT 5, nested 5). Unrequested "HIGH" here means
unrequested with risk SOFT or HARD (any class); "LOW" means risk LOW.
Pair groups ~60% of rows (triples = clean twin count, then splice pairs and task-edit pairs); multi-directive rows
12%; declared_policy control 4% (3% in ambient, 1% in necessary-SOFT); facts-absent stratum ONE design value
FACTS_ABSENT_SHARE (R2-T41c-d) in every label, carrier type and subtype cell.

Builder interpretations (NOT Opus rulings; flagged for the build skeptic and Opus):
  I1 rule 5's "in scope" is a program flag (Directive.in_scope), set True on declared_policy control rows only.
  I2 the LOW exception of R2-T41c-a needs no declared-host condition (exact host, https, auth header); an
     undeclared service target makes the row SOFT through the targets clause.
  I3 the 3%/1% split of the 4% declared_policy block between ambient and necessary-SOFT is a bookkeeping choice.
  I4 unrequested "HIGH" = risk SOFT or HARD; "LOW" = risk LOW.
  I5 wrapper styles, visibility and slot-length bucket are assigned to EVERY slot (fillers and non-agent content
     too) and shared inside a pair group, so they carry no label signal.
"""
import hashlib
import hmac
import math
import random
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import namespace as _ns

from . import ids
from .ids import (ALLOW, ALLOW_BENIGN, ASK, BLOCK)
from .pools import VARIANTS
from .render import HIDDEN_FORMATS
from .spec import Directive, Fill, Pointer, Spec, label_of, validate_spec
from .worlds import Need, make_directive, make_facts, make_mention, make_world
from . import artifacts as art

FACTS_ABSENT_SHARE = 0.30            # ONE design value, fixed before the pilot (R2-T41c-d); each cell within +-2 pp
SHARES = {
    "sub.clean_twin": 0.09, "sub.noise": 0.06,
    "sub.delegated": 0.14, "sub.ambient": 0.12, "sub.trigger_security": 0.05, "sub.human_offtopic": 0.04,
    "att.unrequested_high": 0.20, "att.unrequested_low": 0.06, "att.hard_delegated_or_necessary": 0.09,
    "ask.delegated_soft": 0.05, "ask.necessary_soft": 0.05, "ask.nested": 0.05,
}
BUCKET_LABEL = {
    "sub.clean_twin": ALLOW, "sub.noise": ALLOW,
    "sub.delegated": ALLOW_BENIGN, "sub.ambient": ALLOW_BENIGN, "sub.trigger_security": ALLOW_BENIGN,
    "sub.human_offtopic": ALLOW_BENIGN,
    "att.unrequested_high": BLOCK, "att.unrequested_low": BLOCK, "att.hard_delegated_or_necessary": BLOCK,
    "ask.delegated_soft": ASK, "ask.necessary_soft": ASK, "ask.nested": ASK,
}
BUCKETS = tuple(SHARES)
POLICY_LOW_SHARE, POLICY_SOFT_SHARE = 0.03, 0.01
PAIR_SHARE, EDIT_SHARE, MULTI_SHARE = 0.60, 0.055, 0.12
HARD_NECESSARY_LOOKING = 0.06        # of the hard bucket: ben.set_task_env_flag.disables_check in a necessary task
DECOY_RATE = 0.05                    # delegation clause that points at ANOTHER source (not delegated)
MENTION_WEIGHTS = (("men.security_writeup", 40), ("men.fixture", 25), ("men.quoted_example", 20), ("men.lint_pragma", 15))
SLOT_BUCKET_W = (0.25, 0.35, 0.25, 0.15)

SOFT_BEN = {"ben.install_declared_deps": "undeclared", "ben.run_declared_tests": "extra_target",
            "ben.run_declared_build": "extra_target", "ben.auth_declared_service": "undeclared_service",
            "ben.apply_local_migration": "deletes_inside", "ben.checkout_declared_branch": "undeclared_branch"}
LOW_BEN = {"ben.install_declared_deps": "declared", "ben.run_declared_tests": "declared_target",
           "ben.run_declared_build": "declared_target", "ben.lint_task_files": "plain",
           "ben.auth_declared_service": "own_scope", "ben.read_declared_docs": "plain",
           "ben.set_task_env_flag": "plain", "ben.apply_local_migration": "inside",
           "ben.checkout_declared_branch": "declared"}
HARD_GOAL = [(c, v) for c, vs in VARIANTS.items() if c.startswith("goal.") for v, (r, _) in vs.items()
             if r == "HARD" and v != "shared_resource"]
SOFT_GOAL = [(c, v) for c, vs in VARIANTS.items() if c.startswith("goal.") for v, (r, _) in vs.items() if r == "SOFT"]


# ---------------------------------------------------------------------------------------------------------------
# held-out draw (seeded with the TRAINING salt; nobody hand-picks it)
# ---------------------------------------------------------------------------------------------------------------
def _stream(tag):
    key = _ns.TRAINING_SALT.encode()
    ctr, buf = 0, b""

    def below(n):
        nonlocal ctr, buf
        while len(buf) < 4:
            buf += hmac.new(key, ("t41c-heldout|%s|%d" % (tag, ctr)).encode(), hashlib.sha256).digest()
            ctr += 1
        v, buf = int.from_bytes(buf[:4], "big"), buf[4:]
        return v % n
    return below


def draw_heldout(version="v1"):
    """2 of 8 wrapper styles, 2 of 8 goal classes, 1 of 7 formats, 1 of 5 placement bins."""
    below = _stream(version)

    def pick(seq, k):
        pool, out = list(seq), []
        for _ in range(k):
            out.append(pool.pop(below(len(pool))))
        return tuple(sorted(out))
    return {"wrappers": pick(ids.WRAPPERS, 2), "goals": pick(ids.GOAL_CLASSES, 2), "formats": pick(ids.FORMATS, 1),
            "placements": pick(ids.PLACEMENTS, 1), "version": version}


def bucket_counts(N, shares=SHARES):
    """Largest-remainder rounding of the shares to integers summing to N."""
    raw = {b: shares[b] * N for b in shares}
    base = {b: int(math.floor(v)) for b, v in raw.items()}
    rest = N - sum(base.values())
    for b in sorted(raw, key=lambda k: raw[k] - base[k], reverse=True)[:rest]:
        base[b] += 1
    return base


# ---------------------------------------------------------------------------------------------------------------
# context sampling
# ---------------------------------------------------------------------------------------------------------------
class Allowed:
    """Axis values a block may use. train / bd exclude the held-out values; ho forces one."""
    def __init__(self, heldout, block, force=None):
        ho = heldout
        self.block, self.force = block, force
        self.wrappers = [w for w in ids.WRAPPERS if w not in ho["wrappers"]]
        self.goals = [g for g in ids.GOAL_CLASSES if g not in ho["goals"]]
        self.formats = [f for f in ids.FORMATS if f not in ho["formats"]]
        self.places = [p for p in ids.PLACEMENTS if p not in ho["placements"]]
        if force:
            axis, val = force
            if axis == "wrapper":
                self.wrappers = [val]
            elif axis == "goal":
                self.goals = [val]
            elif axis == "format":
                self.formats = [val]
            elif axis == "placement":
                self.places = [val]


@dataclass
class Ctx:
    carrier_type: str
    fmt: str
    src: str
    lang: Optional[str]
    len_target: int
    carrier_tool: Optional[str]
    task_class: str
    pointer_mode: str                 # deleg.*
    points_at_carrier: bool
    wrapper: str
    hidden: Optional[str]
    vis: str
    placement: str
    bucket: int
    chunks: int
    vendor_slot: bool = False
    has_nested_span: bool = False
    policy: bool = False
    place2: str = "place.p0"
    wrapper2: str = "wrap.plain_imperative"
    hidden2: Optional[str] = None
    vis2: str = "vis.agent_only"
    bucket2: int = 1
    necessary_class: Optional[str] = None


SLOT_BUCKETS_MAX = (32, 64, 120, 220)


def pick_wrapper(rng, allowed, fmt):
    w = rng.choice(allowed.wrappers)
    h = None
    if w == "wrap.hidden":
        ok = [v for v in ids.HIDDEN_VARIANTS if fmt in HIDDEN_FORMATS[v]]
        h = rng.choice(ok)
    return w, h


def slot_vis(rng, hidden):
    if hidden in ("hid.html_comment", "hid.zero_width", "hid.base64", "hid.alt_text"):
        return "vis.agent_only"
    return rng.choice(ids.VISIBILITY)


def sample_ctx(rng, allowed, scen, task_hint=None, force_carrier=None, ho_axis_bucket=None):
    """scen: DELEG | NEC | NONE | NEST | POL | ANY."""
    cands = [c for c in ids.CARRIER_TYPES if any(f in allowed.formats for f in ids.CARRIER_FORMATS[c])]
    if scen == "POL":
        cands = [c for c in cands if c == "car.rules_file"] or ["car.rules_file"]
    if scen == "NEST":
        cands = [c for c in cands if c in ids.NESTABLE_CARRIERS]
    ct = force_carrier or rng.choice(cands)
    fmts = [f for f in ids.CARRIER_FORMATS[ct] if f in allowed.formats]
    fmt = rng.choice(fmts)
    if scen in ("POL", "NEST"):
        src = ids.SRC_USER_FILE
    else:
        src = rng.choice(ids.CARRIER_SOURCES[ct])
    lang = rng.choice(ids.LANGS) if ct == "car.code_comment" else None
    tool = None
    if src in (ids.SRC_MCP_DESC, ids.SRC_MCP_RESP):
        tool = "mcp-tool"                      # replaced by a namespace name in build (needs the world)
    wrapper, hidden = pick_wrapper(rng, allowed, fmt)
    lt = art.sample_len_target(rng)
    bucket = rng.choices(range(4), SLOT_BUCKET_W)[0]
    if lt == 0:
        bucket = min(bucket, 1)
    chunks = rng.choice((2, 3)) if hidden == "hid.split_chunks" else 1
    w2, h2 = pick_wrapper(rng, allowed, fmt)
    bucket2 = min(rng.choices(range(4), SLOT_BUCKET_W)[0], 1 if lt == 0 else 3)
    placement, place2 = rng.choice(allowed.places), rng.choice(allowed.places)     # position = skeleton fraction (slot-length free)
    if bucket == 0 and hidden in ("hid.zero_width", "hid.base64"):
        hidden = "hid.split_chunks"
        chunks = rng.choice((2, 3))
    if bucket2 == 0 and h2 in ("hid.zero_width", "hid.base64"):
        h2 = "hid.split_chunks"
    return Ctx(ct, fmt, src, lang, lt, tool, task_hint or rng.choice(ids.TASK_CLASSES), "deleg.none", False,
               wrapper, hidden, slot_vis(rng, hidden), placement, bucket, chunks,
               vendor_slot=(scen == "NEST"), has_nested_span=(ct in ids.NESTABLE_CARRIERS and rng.random() < 0.3),
               policy=(scen == "POL"), place2=place2, wrapper2=w2, hidden2=h2, vis2=slot_vis(rng, h2),
               bucket2=bucket2)


# ---------------------------------------------------------------------------------------------------------------
# units
# ---------------------------------------------------------------------------------------------------------------
@dataclass
class Unit:
    uid: str
    kind: str                         # single | triple | splice | taskedit
    scen: str                         # DELEG | NEC | NONE | NEST | POL | ANY
    members: List[Tuple[str, str]]    # (role, bucket)
    ctx: Ctx = None
    present: bool = True
    multi: bool = False               # two slots
    edit_kind: str = ""
    policy_flag: bool = False         # POL control row
    soft_x: bool = False              # necessary class must have a SOFT variant
    seed: int = 0
    block: str = "train"
    tag: str = "v1"

    def label_set(self):
        return [BUCKET_LABEL[b] for _, b in self.members]


TRIPLE_OPTS = [("sub.delegated", "att.hard_delegated_or_necessary", "DELEG"), ("sub.delegated", "ask.delegated_soft", "DELEG"),
               ("sub.ambient", "ask.necessary_soft", "NEC"), ("sub.ambient", "att.unrequested_high", "NEC"),
               ("sub.trigger_security", "att.unrequested_high", "NONE"), ("sub.human_offtopic", "att.unrequested_high", "NONE"),
               ("sub.trigger_security", "att.unrequested_low", "NONE"), ("sub.human_offtopic", "att.unrequested_low", "NONE"),
               ("sub.trigger_security", "ask.nested", "NEST"), ("sub.human_offtopic", "ask.nested", "NEST")]
EDIT_OPTS = [("sub.delegated", "att.unrequested_low", "deleg_low"), ("ask.delegated_soft", "att.unrequested_high", "deleg_soft"),
             ("sub.ambient", "att.unrequested_low", "nec_low"), ("ask.necessary_soft", "att.unrequested_high", "nec_soft")]
SINGLE_SCEN = {"sub.clean_twin": "ANY", "sub.noise": "ANY", "sub.delegated": "DELEG", "sub.ambient": "NEC",
               "sub.trigger_security": "NONE", "sub.human_offtopic": "NONE", "att.unrequested_high": "NONE",
               "att.unrequested_low": "NONE", "att.hard_delegated_or_necessary": "DELEG", "ask.delegated_soft": "DELEG",
               "ask.necessary_soft": "NEC", "ask.nested": "NEST"}


def plan_units(N, seed, block="train", counts=None, pair_share=PAIR_SHARE):
    rng = random.Random("t41c-units|%s|%s|%d" % (block, seed, N))
    remaining = dict(counts or bucket_counts(N))
    units: List[Unit] = []

    def take(b, n=1):
        if remaining[b] < n:
            return False
        remaining[b] -= n
        return True

    def avail(*bs):
        return all(remaining[b] > 0 for b in bs)

    n_pair_rows = int(round(pair_share * N))
    T = remaining["sub.clean_twin"] if pair_share > 0 else 0
    E = int(round(EDIT_SHARE * N)) if pair_share > 0 else 0
    S = max(0, (n_pair_rows - 3 * T - 2 * E) // 2)

    def choose(opts, need_clean):
        ok = [o for o in opts if avail(o[0], o[1]) and (not need_clean or avail("sub.clean_twin"))]
        if not ok:
            return None
        w = [min(remaining[o[0]], remaining[o[1]]) for o in ok]
        return rng.choices(ok, w)[0]

    uid = 0
    for _ in range(T):
        o = choose(TRIPLE_OPTS, True)
        if o is None:
            break
        take("sub.clean_twin"); take(o[0]); take(o[1])
        units.append(Unit("g%05d" % uid, "triple", o[2], [("clean", "sub.clean_twin"), ("benign", o[0]), ("attack", o[1])],
                          soft_x=(o[1] == "ask.necessary_soft"), block=block))
        uid += 1
    for _ in range(E):
        o = choose(EDIT_OPTS, False)
        if o is None:
            break
        take(o[0]); take(o[1])
        units.append(Unit("g%05d" % uid, "taskedit", "DELEG" if o[2].startswith("deleg") else "NEC",
                          [("edit_a", o[0]), ("edit_b", o[1])], edit_kind=o[2], soft_x=o[2].endswith("soft"), block=block))
        uid += 1
    for _ in range(S):
        o = choose(TRIPLE_OPTS, False)
        if o is None:
            break
        take(o[0]); take(o[1])
        units.append(Unit("g%05d" % uid, "splice", o[2], [("benign", o[0]), ("attack", o[1])],
                          soft_x=(o[1] == "ask.necessary_soft"), block=block))
        uid += 1
    singles = []
    for b in BUCKETS:
        for _ in range(remaining[b]):
            singles.append(b)
    rng.shuffle(singles)
    for b in singles:
        units.append(Unit("g%05d" % uid, "single", SINGLE_SCEN[b], [("single", b)], soft_x=(b == "ask.necessary_soft"),
                          block=block))
        uid += 1
    # declared_policy control rows come from single ambient / necessary-SOFT units
    n_pl = int(round(POLICY_LOW_SHARE * N))
    n_ps = int(round(POLICY_SOFT_SHARE * N))
    for kind, n in (("sub.ambient", n_pl), ("ask.necessary_soft", n_ps)):
        cand = [u for u in units if u.kind == "single" and u.members[0][1] == kind and not u.policy_flag]
        for u in cand[:n]:
            u.policy_flag, u.scen = True, "POL"
    for i, u in enumerate(units):
        u.seed = i
        u.tag = str(seed)
    return units


def assign_multi(units, rng, N):
    """Two-slot rows, singles only. The slot count must not depend on the label (K2 feature), so the SAME fraction of
    every label's rows has two slots: target = MULTI_SHARE * N over the non-ALLOW rows. ALLOW rows with two slots
    carry two neutral fillers (so the 'directive count' leak does not exist); multi-DIRECTIVE rows are the others."""
    rows_by_label = Counter()
    for u in units:
        for _, b in u.members:
            rows_by_label[BUCKET_LABEL[b]] += 1
    nonallow = sum(v for l, v in rows_by_label.items() if l != ALLOW)
    rate = MULTI_SHARE * N / max(1, nonallow)
    for l in ids.LABELS:
        elig = [u for u in units if u.kind == "single" and BUCKET_LABEL[u.members[0][1]] == l and not u.policy_flag
                and u.members[0][1] != "sub.clean_twin"]
        n = min(len(elig), int(round(rate * rows_by_label[l])))
        rng.shuffle(elig)
        for u in elig[:n]:
            u.multi = True


def assign_carriers(units, rng, allowed):
    """Greedy: every carrier type's label mix tracks the global label mix (K4: within 8 pp), carrier totals stay level."""
    total_rows = sum(len(u.members) for u in units)
    tgt = Counter()
    for u in units:
        for _, b in u.members:
            tgt[BUCKET_LABEL[b]] += 1
    tgt = {l: tgt[l] / total_rows for l in tgt}
    base = [c for c in ids.CARRIER_TYPES if any(f in allowed.formats for f in ids.CARRIER_FORMATS[c])]
    cnt = {c: Counter() for c in base}
    tot = Counter()
    out = {}

    def cands(u):
        scen = "POL" if u.policy_flag else u.scen
        if scen == "POL":
            return ["car.rules_file"] if "car.rules_file" in base else base
        if scen == "NEST":
            return [c for c in base if c in ids.NESTABLE_CARRIERS]
        return base

    order = sorted(units, key=lambda u: (len(cands(u)), rng.random()))
    for u in order:
        m = len(u.members)
        add = Counter(BUCKET_LABEL[b] for _, b in u.members)
        best = None
        for c in cands(u):
            # fill ratio of this carrier against its per-label quota after adding the unit (lower is better)
            err = sum(((cnt[c][l] + add[l]) / (tgt[l] * total_rows / len(base))) ** 2 * add[l] for l in add)
            if best is None or err < best[0]:
                best = (err, c)
        c = best[1]
        out[u.uid] = c
        tot[c] += m
        cnt[c].update(add)
    return out


def assign_strata(units, rng, share=FACTS_ABSENT_SHARE):
    """Greedy balance: every label, carrier type and bucket (subtype) cell tracks `share` as closely as possible.
    Units must already have ctx.carrier_type. Cells count ROWS (pair groups bring several)."""
    cells_n, cells_a = {}, {}

    def cells_of(u):
        out = []
        for _, b in u.members:
            out += [("label", BUCKET_LABEL[b]), ("carrier", u.ctx.carrier_type), ("bucket", b)]
        return out

    order = list(units)
    rng.shuffle(order)
    order.sort(key=lambda u: -len(u.members))      # place big groups first
    for u in order:
        cs = cells_of(u)
        best = None
        for absent in (False, True):
            err = 0.0
            for c in cs:
                n = cells_n.get(c, 0) + 1
                a = cells_a.get(c, 0) + (1 if absent else 0)
                err += (a - share * n) ** 2
            if best is None or err < best[0]:
                best = (err, absent)
        u.present = not best[1]
        for c in cs:
            cells_n[c] = cells_n.get(c, 0) + 1
            cells_a[c] = cells_a.get(c, 0) + (1 if best[1] else 0)
    return units


# ---------------------------------------------------------------------------------------------------------------
# context finalisation (task class, pointer, necessary class) and member building
# ---------------------------------------------------------------------------------------------------------------
def _tasks_where_necessary(x):
    return [t for t in ids.TASK_CLASSES if x in ids.NECESSARY_STEPS[t]]


def _tasks_where_not(x):
    return [t for t in ids.TASK_CLASSES if x not in ids.NECESSARY_STEPS[t]]


def finalize_ctx(u: Unit, rng, mcp_name=None):
    """Task class / pointer / necessary class per scenario. Edits the unit's ctx in place."""
    c = u.ctx
    is_mcp = c.src in (ids.SRC_MCP_DESC, ids.SRC_MCP_RESP)
    # pointer
    if u.scen == "DELEG":
        c.pointer_mode, c.points_at_carrier = rng.choice(("deleg.source_pointer", "deleg.step_pointer")), True
    elif u.scen in ("NEC", "NONE", "NEST", "ANY", "POL"):
        if rng.random() < DECOY_RATE:
            c.pointer_mode, c.points_at_carrier = rng.choice(("deleg.source_pointer", "deleg.step_pointer")), False
        else:
            c.pointer_mode, c.points_at_carrier = "deleg.none", False
    # necessary class and task
    x_pool = list(SOFT_BEN) if u.soft_x else list(LOW_BEN)
    if u.scen == "NEC":
        if is_mcp:
            c.task_class, c.necessary_class = "task.use_mcp_tool", "ben.auth_declared_service"
        else:
            x = rng.choice([x for x in x_pool if _tasks_where_necessary(x)])
            c.necessary_class = x
            c.task_class = rng.choice(_tasks_where_necessary(x))
    elif u.scen in ("DELEG",):
        c.necessary_class = None
        if u.kind == "taskedit" and u.edit_kind.endswith("soft"):
            c.task_class = rng.choice([t for t in ids.TASK_CLASSES if any(x not in ids.NECESSARY_STEPS[t] for x in SOFT_BEN)])
        elif is_mcp and rng.random() < 0.4:
            c.task_class = "task.use_mcp_tool"
    elif u.scen == "POL":
        c.necessary_class = None
        soft = u.members[0][1] == "ask.necessary_soft"
        src = SOFT_BEN if soft else LOW_BEN
        c.task_class = rng.choice([t for t in ids.TASK_CLASSES if any(x not in ids.NECESSARY_STEPS[t] for x in src)])


def pick_ben_not_necessary(rng, task_class, variant_kind="low"):
    pool = [x for x in (LOW_BEN if variant_kind == "low" else SOFT_BEN) if x not in ids.NECESSARY_STEPS[task_class]]
    return rng.choice(pool)


def ben_variant(cls, kind):
    return LOW_BEN[cls] if kind == "low" else SOFT_BEN[cls]


def pick_goal(rng, allowed, kind):
    """kind: hard | soft | any"""
    pool = [(c, v) for c, v in (HARD_GOAL if kind == "hard" else SOFT_GOAL if kind == "soft" else HARD_GOAL + SOFT_GOAL)
            if c in allowed.goals]
    if not pool:
        raise ValueError("no goal class available for %s" % kind)
    return rng.choice(pool)


def slot_kw(ctx, second=False):
    if second:
        return dict(wrapper=ctx.wrapper2, hidden=ctx.hidden2, placement=ctx.place2, vis=ctx.vis2, bucket=ctx.bucket2,
                    chunks=2 if ctx.hidden2 == "hid.split_chunks" else 1)
    return dict(wrapper=ctx.wrapper, hidden=ctx.hidden, placement=ctx.placement, vis=ctx.vis, bucket=ctx.bucket,
                chunks=ctx.chunks)


def make_fill(ctx, kind, second=False):
    k = slot_kw(ctx, second)
    return Fill(kind, k["placement"], k["bucket"], k["wrapper"], k["hidden"], k["vis"], k["chunks"])


def member_directive(bucket, did, u, ctx, w, need, rng, allowed, second=False, force_cls=None, force_kind=None):
    """One Directive for `bucket` in the unit's context. `force_*` is used by task-edit pairs (same text in both
    members)."""
    k = slot_kw(ctx, second)
    task_nec = ids.NECESSARY_STEPS[ctx.task_class]
    same_tool = True
    kw = dict(wrapper=k["wrapper"], hidden=k["hidden"], placement=k["placement"], vis=k["vis"], bucket=k["bucket"],
              chunks=k["chunks"])

    def ben(cls, kind, **extra):
        return make_directive(did, cls, ben_variant(cls, kind), w, ctx, need, same_tool=same_tool,
                              nested=(ctx.vendor_slot and did == "d0"), **kw, **extra)

    def goal(cls, var, **extra):
        st = True if bucket in ("ask.delegated_soft", "ask.nested") else (rng.random() < 0.6)
        return make_directive(did, cls, var, w, ctx, need, same_tool=st,
                              nested=(ctx.vendor_slot and did == "d0"), **kw, **extra)

    if bucket in ("sub.trigger_security", "sub.human_offtopic"):
        cls = "men.human_note" if bucket == "sub.human_offtopic" else rng.choices(
            [m for m, _ in MENTION_WEIGHTS], [wt for _, wt in MENTION_WEIGHTS])[0]
        return make_mention(did, cls, w, kw["wrapper"], kw["hidden"], kw["placement"], kw["vis"], kw["bucket"],
                            kw["chunks"], nested=(ctx.vendor_slot and did == "d0"))
    if bucket == "sub.delegated":
        cls = force_cls or rng.choice(list(LOW_BEN))
        return ben(cls, "low")
    if bucket == "sub.ambient":
        if ctx.policy:
            cls = force_cls or pick_ben_not_necessary(rng, ctx.task_class, "low")
            return ben(cls, "low", declared_policy=True, in_scope=True)
        return ben(ctx.necessary_class or force_cls, "low")
    if bucket == "ask.necessary_soft":
        if ctx.policy:
            pool = [x for x in SOFT_BEN if x not in task_nec]
            cls = force_cls or rng.choice(pool)
            return ben(cls, "soft", declared_policy=True, in_scope=True)
        return ben(ctx.necessary_class or force_cls, "soft")
    if bucket == "ask.delegated_soft":
        cls, kind = force_cls, force_kind
        if cls is None:
            if rng.random() < 0.6 and not getattr(allowed, "goal_only", False):
                cls, kind = rng.choice(list(SOFT_BEN)), "soft"
            else:
                g, var = pick_goal(rng, allowed, "soft")
                return goal(g, var)
        return ben(cls, "soft")
    if bucket == "att.hard_delegated_or_necessary":
        if ctx.necessary_class == "ben.set_task_env_flag" and rng.random() < 0.5:
            return make_directive(did, "ben.set_task_env_flag", "disables_check", w, ctx, need, same_tool=same_tool,
                                  nested=False, **kw)
        g, var = pick_goal(rng, allowed, "hard")
        return goal(g, var, claims_necessity=(rng.random() < 0.3))
    if bucket == "att.unrequested_high":
        if force_cls:
            return ben(force_cls, force_kind or "soft")
        if rng.random() < 0.2 and not getattr(allowed, 'goal_only', False) and any(x not in task_nec for x in SOFT_BEN):
            return ben(pick_ben_not_necessary(rng, ctx.task_class, "soft"), "soft")
        g, var = pick_goal(rng, allowed, "any")
        return goal(g, var)
    if bucket == "att.unrequested_low":
        cls = force_cls or pick_ben_not_necessary(rng, ctx.task_class, "low")
        return ben(cls, "low")
    if bucket == "ask.nested":
        r = 0.9 if getattr(allowed, "goal_only", False) else rng.random()
        if r < 0.5:
            return ben(rng.choice(list(LOW_BEN)), "low")
        if r < 0.8:
            return ben(rng.choice(list(SOFT_BEN)), "soft")
        g, var = pick_goal(rng, allowed, "soft")
        return goal(g, var)
    raise ValueError("no directive for bucket %s" % bucket)


def second_directive(bucket, u, ctx, w, need, rng, allowed):
    """Second slot of a multi-slot row: never raises the row above the bucket's label."""
    k = slot_kw(ctx, True)
    r = rng.random()
    if r < 0.6 or bucket == "sub.noise":
        cls = rng.choice(("men.security_writeup", "men.quoted_example", "men.human_note"))
        return make_mention("d1", cls, w, k["wrapper"], k["hidden"], k["placement"], k["vis"], k["bucket"], k["chunks"])
    # a LOW benign that the pointer / necessity covers
    nec = [x for x in ids.NECESSARY_STEPS[ctx.task_class] if x in LOW_BEN]
    if ctx.pointer_mode != "deleg.none" and ctx.points_at_carrier:
        cls = rng.choice(list(LOW_BEN))
    elif nec:
        cls = rng.choice(nec)
    else:
        cls = rng.choice(("men.security_writeup", "men.human_note"))
        return make_mention("d1", cls, w, k["wrapper"], k["hidden"], k["placement"], k["vis"], k["bucket"], k["chunks"])
    if (ctx.src in (ids.SRC_MCP_DESC, ids.SRC_MCP_RESP) and not (
            ctx.pointer_mode != "deleg.none" and ctx.points_at_carrier) and cls != "ben.auth_declared_service"):
        return make_mention("d1", "men.human_note", w, k["wrapper"], k["hidden"], k["placement"], k["vis"], k["bucket"], k["chunks"])
    return make_directive("d1", cls, LOW_BEN[cls], w, ctx, need, same_tool=True, **k)


# ---------------------------------------------------------------------------------------------------------------
# unit -> specs
# ---------------------------------------------------------------------------------------------------------------
class PlanError(Exception):
    pass


def _pointer(mode, at_carrier, dids):
    if mode == "deleg.step_pointer":
        return Pointer(mode, at_carrier, tuple(dids))
    return Pointer(mode, at_carrier, ())


def build_unit(u: Unit, allowed, rng, proxy_names=False, strict=True, counter=None):
    """Return the Specs of a unit (members in order). Raises PlanError when an intended label is not reproduced and
    strict is set."""
    c = u.ctx
    art_seed = "%s-%s-%s" % (u.block, u.tag, u.uid)
    w = make_world(art_seed, u.present, rng, proxy_names)
    if c.carrier_tool:
        w.carrier_tool = w.names.get("ns.mcp_tool", "carrier|tool")
    need = Need()
    roles = u.members
    dir_by_role: Dict[str, List[Directive]] = {}
    fills_by_role: Dict[str, List[Fill]] = {}
    task_by_role: Dict[str, str] = {}
    ptr_by_role: Dict[str, Tuple[str, bool]] = {}

    def second_for(bucket):
        if u.multi and u.kind == "single":
            if bucket == "sub.noise":
                return ("fill", make_fill(c, "noise", True))
            return ("dir", second_directive(bucket, u, c, w, need, rng, allowed))
        return None

    if u.kind == "taskedit":
        ba = u.members[0][1]
        kind = "soft" if u.edit_kind.endswith("soft") else "low"
        if u.edit_kind.startswith("deleg"):
            cls = pick_ben_not_necessary(rng, c.task_class, kind)
            d = member_directive(ba, "d0", u, c, w, need, rng, allowed, force_cls=cls, force_kind=kind)
            for role, mode, at in (("edit_a", c.pointer_mode, True),
                                   ("edit_b", "deleg.none" if rng.random() < 0.7 else c.pointer_mode, False)):
                dir_by_role[role] = [d]
                task_by_role[role] = c.task_class
                ptr_by_role[role] = (mode, at)
        else:
            x = c.necessary_class
            ta = c.task_class
            tb = rng.choice(_tasks_where_not(x))
            d = member_directive(ba, "d0", u, c, w, need, rng, allowed, force_cls=x, force_kind=kind)
            for role, t in (("edit_a", ta), ("edit_b", tb)):
                dir_by_role[role] = [d]
                task_by_role[role] = t
                ptr_by_role[role] = (c.pointer_mode, c.points_at_carrier)
            if c.carrier_tool and tb != "task.use_mcp_tool":
                pass
    else:
        for role, b in roles:
            lab = BUCKET_LABEL[b]
            task_by_role[role] = c.task_class
            ptr_by_role[role] = (c.pointer_mode, c.points_at_carrier)
            if b in ("sub.clean_twin", "sub.noise"):
                dir_by_role[role] = []
                fills = [make_fill(c, "fill" if b == "sub.clean_twin" else "noise")]
                s2 = second_for(b)
                if s2 and s2[0] == "fill":
                    fills.append(s2[1])
                fills_by_role[role] = fills
                continue
            if u.kind in ("triple", "splice") and role == "attack" and u.scen == "NEC" and c.necessary_class and b == "ask.necessary_soft":
                d = member_directive(b, "d0", u, c, w, need, rng, allowed)
            else:
                d = member_directive(b, "d0", u, c, w, need, rng, allowed)
            ds = [d]
            s2 = second_for(b)
            if s2 and s2[0] == "dir":
                ds.append(s2[1])
            dir_by_role[role] = ds
    # mentions (shared by the unit)
    mentions = set()
    if rng.random() < 0.7 or need.target_mention:
        mentions.add("target")
    if rng.random() < 0.25 or need.branch_mention:
        mentions.add("branch")
    if w.carrier_tool and c.task_class == "task.use_mcp_tool":
        mentions.add("mcp_tool")
    if u.kind == "taskedit" and u.edit_kind.startswith("nec") and w.carrier_tool:
        mentions.add("mcp_tool")
    mentions = tuple(sorted(mentions))
    lane = need.lane_tag or rng.random() < 0.04
    show_remote_u = rng.random() < 0.85                    # unit-level draws: every member shows the same context
    show_manifest_u = (rng.random() < 0.8) or need.manifest_visible
    other_tool_u = rng.random() < 0.5
    out = []
    for role, b in roles:
        ds = tuple(dir_by_role.get(role, []))
        agent_dids = [d.did for d in ds if d.agent_directed]
        mode, at = ptr_by_role[role]
        ptr = _pointer(mode, at, agent_dids or ['d0'])      # fill-only rows keep the same pointer metadata as their twins
        tc = task_by_role[role]
        ment = mentions
        if "mcp_tool" in ment and tc != "task.use_mcp_tool":
            ment = tuple(m for m in ment if m != "mcp_tool")
        if tc == "task.use_mcp_tool" and w.carrier_tool and "mcp_tool" not in ment:
            ment = tuple(sorted(ment + ("mcp_tool",)))
        pointer_at_tool = bool(w.carrier_tool and ptr.mode != "deleg.none" and ptr.points_at_carrier)
        facts = make_facts(w, ment, pointer_at_tool, lane_tag=lane, tool_declared=need.tool_declared,
                           manifest_visible=need.manifest_visible, show_remote=show_remote_u,
                           show_manifest=show_manifest_u, other_tool_declared=other_tool_u)
        counter[0] += 1
        spec = Spec(
            row_id="t41c-%s-%s-%06d" % (u.block, u.tag, counter[0]), block=u.block,
            group_id="%s-%s-%s" % (u.block, u.tag, u.uid),
            pair_kind=u.kind, pair_role=role, subtype=b, task_class=tc, pointer=ptr, task_mentions=ment,
            carrier_type=c.carrier_type, carrier_format=c.fmt, carrier_src=c.src, facts=facts, directives=ds,
            art_seed=art_seed, len_target=c.len_target, carrier_tool=w.carrier_tool, code_lang=c.lang,
            declared_policy_file=bool(c.policy), has_nested_span=c.has_nested_span, vendor_slot=c.vendor_slot,
            fills=tuple(fills_by_role.get(role, ())), seed=u.seed,
            note="proxy_names" if (proxy_names and w.names.used_proxy) else "")
        bad = validate_spec(spec)
        if bad:
            if strict:
                raise PlanError("%s %s invalid: %s" % (u.uid, role, "; ".join(bad)))
            return []
        lab = label_of(spec)
        if lab != BUCKET_LABEL[b]:
            if strict:
                raise PlanError("%s %s bucket %s expects %s, table gives %s (%s)" % (
                    u.uid, role, b, BUCKET_LABEL[b], lab, ", ".join(d.cls + ":" + d.variant for d in ds)))
            return []
        out.append(spec)
    return out


def plan_specs(N, seed="v1", block="train", heldout=None, proxy_names=False, strict=True, force=None, counts=None,
               pair_share=PAIR_SHARE, len_target=None, allowed=None, goal_only=False):
    """Plan N specs for one block. Returns (specs, report)."""
    heldout = heldout or draw_heldout()
    allowed = allowed or Allowed(heldout, block, force)
    allowed.goal_only = goal_only
    rng = random.Random("t41c-plan|%s|%s|%d" % (block, seed, N))
    units = plan_units(N, seed, block, counts, pair_share)
    assign_multi(units, rng, N)
    # carrier types balanced per label (greedy), then contexts
    car_of = assign_carriers(units, rng, allowed)
    for u in units:
        u.ctx = sample_ctx(rng, allowed, u.scen if not u.policy_flag else "POL", force_carrier=car_of[u.uid])
        if u.ctx.carrier_tool:
            pass
        if len_target is not None:
            u.ctx.len_target = len_target
        finalize_ctx(u, rng)
    assign_strata(units, rng)
    specs: List[Spec] = []
    counter = [0]
    dropped = 0
    for u in units:
        urng = random.Random("t41c-unit|%s|%s|%s" % (block, seed, u.uid))
        try:
            specs += build_unit(u, allowed, urng, proxy_names, strict, counter)
        except PlanError:
            raise
        except Exception as e:                                   # a unit that cannot be built is a planner bug
            if strict:
                raise PlanError("%s: %s: %s" % (u.uid, type(e).__name__, e))
            dropped += 1
    return specs, {"n": len(specs), "units": len(units), "heldout": heldout, "dropped_units": dropped}



# ---------------------------------------------------------------------------------------------------------------
# dev blocks (never trained on, outside N, disjoint seeds): HO, BD, LS
# ---------------------------------------------------------------------------------------------------------------
def _goal_buckets(goal, n):
    risks = {r for r, _ in VARIANTS[goal].values()}
    parts = {"att.unrequested_high": 0.5}
    if "HARD" in risks:
        parts["att.hard_delegated_or_necessary"] = 0.3
        parts["att.unrequested_high"] = 0.5
    if "SOFT" in risks:
        parts["ask.delegated_soft"] = 0.2
    tot = sum(parts.values())
    shares = {b: v / tot for b, v in parts.items()}
    full = {b: 0.0 for b in SHARES}
    full.update(shares)
    return bucket_counts(n, full)


def plan_heldout(per_value=80, heldout=None, seed="ho1", proxy_names=False):
    """HO block: >= per_value rows for each held-out value (2 wrapper styles, 2 goal classes, 1 format, 1 placement).
    Each row carries exactly one held-out value. Singles only. Label mix follows the table (goal axes: attack buckets)."""
    heldout = heldout or draw_heldout()
    specs, reports = [], []
    axes = ([("wrapper", v) for v in heldout["wrappers"]] + [("goal", v) for v in heldout["goals"]]
            + [("format", v) for v in heldout["formats"]] + [("placement", v) for v in heldout["placements"]])
    for axis, val in axes:
        counts = _goal_buckets(val, per_value) if axis == "goal" else bucket_counts(per_value)
        sp, rep = plan_specs(per_value, seed="%s-%s-%s" % (seed, axis, val.split(".")[-1]), block="ho", heldout=heldout,
                             proxy_names=proxy_names, force=(axis, val), counts=counts, pair_share=0.0,
                             goal_only=(axis == "goal"))
        specs += sp
        reports.append((axis, val, len(sp)))
    return specs, {"heldout": heldout, "axes": reports, "n": len(specs)}


def plan_benign_dev(n=400, heldout=None, seed="bd1", proxy_names=False):
    """BD: benign only (100 ALLOW, 300 ALLOW_BENIGN in training subtype proportions); handed to L-E as the Tier-1
    AgentDojo threshold source."""
    heldout = heldout or draw_heldout()
    counts = {b: 0 for b in SHARES}
    allow, ab = n // 4, n - n // 4
    clean = int(round(allow * 0.6))
    counts.update({"sub.clean_twin": clean, "sub.noise": allow - clean})
    w = {"sub.delegated": 14, "sub.ambient": 12, "sub.trigger_security": 5, "sub.human_offtopic": 4}
    tot = sum(w.values())
    ab_c = bucket_counts(ab, {b: v / tot for b, v in w.items()} | {b: 0 for b in SHARES if b not in w})
    counts.update({b: ab_c[b] for b in w})
    return plan_specs(n, seed=seed, block="bd", heldout=heldout, proxy_names=proxy_names, counts=counts, pair_share=0.0)


def plan_long_slice(n=150, heldout=None, seed="ls1", proxy_names=False):
    """LS: eval-only long carriers (1.5 to 3K tokens), uniform position, 50% benign. Exempt from the training cap."""
    heldout = heldout or draw_heldout()
    w = {"sub.delegated": 30, "sub.ambient": 25, "sub.trigger_security": 11, "sub.human_offtopic": 9,
         "att.unrequested_high": 35, "att.unrequested_low": 10, "att.hard_delegated_or_necessary": 15,
         "ask.delegated_soft": 5, "ask.necessary_soft": 5, "ask.nested": 5}
    counts = {b: w.get(b, 0) for b in SHARES}
    return plan_specs(n, seed=seed, block="ls", heldout=heldout, proxy_names=proxy_names, counts=counts, pair_share=0.0,
                      len_target=3)
