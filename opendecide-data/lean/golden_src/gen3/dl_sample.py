"""dl_sample: the constructive sampler of yn2b family F6 `gen3_def_literal`. It draws a definition and a fact pattern
aimed at a target (the builder picks the stratum first, then the gold, SPEC 4.6), and returns the facts only: the
builder re-labels every item with dl_core.decide() and drops it if decide() does not give the target (no label is ever
taken from here).

Targets (ctx):
  truth   the item's answer to "is it a <term>?" (yes/no, JB and judge latents; judge gold = record == truth)
  dk      how the outcome is decided: truth True -> path (the elements hold) | deem (the deeming clause holds while
          the elements fail) | rincl (the outside rule, written into the definition as the deeming clause, holds);
          truth False -> elem (the elements fail) | excl (a stated exclusion applies) | rexcl (the outside rule,
          written in as an exclusion, applies)
  excg    the SPEC 4.6 exception group to build in (allow_deny | deny_allow | near_miss | None)
  miss    "decisive" | "irrelevant" | None: a value the file does not record, that decides the outcome or not
  r_place none | facts | card | both: where the outside rule appears (card only when it decides the outcome)
  usage_agree   whether the everyday-usage statement agrees with the outcome
  r_agree       whether the outside rule (when it is not in the definition) agrees with the outcome
  choice  only for the choice view: the AND definition has exactly one failing condition (or none)
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import dl_core as dc  # noqa: E402
import dl_packs as dp  # noqa: E402
import mv_core as mv  # noqa: E402

TIER_KNOBS = {  # n elements, n exclusions (weights), P(unless | exclusion), P(native deeming clause), extra facts
    "easy": {"n_el": (2,), "n_ex": {0: 0.6, 1: 0.4}, "unless": 0.0, "deem": 0.0, "irrelevant": (1,),
             "neutral": (0, 1)},
    "standard": {"n_el": (2, 3), "n_ex": {0: 0.4, 1: 0.6}, "unless": 0.35, "deem": 0.12, "irrelevant": (1, 2),
                 "neutral": (0, 1)},
    "judge": {"n_el": (2, 3), "n_ex": {0: 0.4, 1: 0.6}, "unless": 0.35, "deem": 0.12, "irrelevant": (1, 2),
              "neutral": (0, 1)},
    "hard": {"n_el": (3, 4), "n_ex": {1: 0.6, 2: 0.4}, "unless": 0.5, "deem": 0.2, "irrelevant": (1, 2),
             "neutral": (0, 1, 1)},
}
OPS = (">=", ">", "<=", "<")
# R2 fix (1 Oct): P(a deeming clause | the term does not apply). Items that count got one from the deem / rincl plans
# (0.38) plus the native share of path items, items that do not count only the native 12-20%, so "a deeming clause is
# printed -> it counts" was right on 69% of train rows. A failing deeming clause is now as common on 'no' items.
DEEM_FALSE = {"easy": 0.38, "standard": 0.46, "judge": 0.46, "hard": 0.5}


class SampleFail(Exception):
    pass


# ------------------------------------------------------------------------------------------------ coherence (R2 fix)
MIN_MEMBER_AGE = 8          # club: years of membership <= age - 8
MIN_ACADEMY_AGE = 6         # sports: years in the academy <= age - 6
ADULT_AGE = 17              # tenancy: an occupant under 17 is not on the lease, pays no rent, parks no vehicle, and
MINOR_RELATIONS = ("child", "sibling")   # is the tenant's child or sibling
WORKDAY_HOURS = 8           # safety: every day off work after the first costs at least a working day of hours


def _report_day(f: dict, aid: str, v: int) -> int:
    """The day the file could first know of a date fact: the event day, plus the reporting delay where the file
    states one (insurance: days taken to report; safety: hours to report)."""
    vals = f["values"]
    if f["pack"] == "insurance" and aid == "date" and vals.get("reported") is not None:
        return v + vals["reported"]
    if f["pack"] == "safety" and aid == "date" and vals.get("reported") is not None:
        return v + (vals["reported"] + 23) // 24
    return v


def date_floor(f: dict) -> int:
    """The earliest day the file can have been opened: after every date fact (and its report)."""
    A = {a.id: a for a in dp.PACKS[f["pack"]].attrs}
    days = [_report_day(f, k, v) for k, v in f["values"].items() if v is not None and A[k].kind == "date"]
    return max(days) + 1 if days else 1


def in_force_day(pack: dp.Pack, x: int) -> int:
    """The JB definition's 'in force from' day: x in 1..45 scaled below the pack's earliest possible date fact, so a
    governing definition is always in force before every date the file can state (twins included)."""
    lo = [a.lo for a in pack.attrs if a.kind == "date"]
    cap = max(1, min([45] + [d - 1 for d in lo]))
    return 1 + (x - 1) * (cap - 1) // 44


def opened_day(f: dict, x: int) -> int:
    """The file's opening day: x (60..335) moved after every date fact when it would precede one."""
    floor = date_floor(f)
    return x if x >= floor else min(365, floor + x % 21)


def incoherent(f: dict) -> str | None:
    """None when the facts of one file are mutually consistent, else the rule they break (R2 coherence hunt: a fact
    pattern that contradicts itself gives a reader a reading under which the gold is wrong)."""
    v, pack = f["values"], f["pack"]
    for grp in dp.EXCLUSIVE_ATTRS.get(pack, ()):
        if sum(1 for a in grp if a in f.get("order", ())) > 1:
            return "linked attributes shown together"
    age = v.get("age")
    if age is not None:
        if pack == "club" and v.get("membership") is not None and v["membership"] > age - MIN_MEMBER_AGE:
            return "membership longer than the age allows"
        if pack == "sports" and ((v.get("residence") is not None and v["residence"] > age) or
                                 (v.get("academy") is not None and v["academy"] > age - MIN_ACADEMY_AGE)):
            return "residence / academy longer than the age allows"
        if pack == "tenancy":
            if v.get("months") is not None and v["months"] > 12 * age:
                return "stay longer than the age allows"
            if age < ADULT_AGE and (v.get("on_lease") is True or v.get("vehicle") is True or (v.get("rent_share") or 0)
                                    > 0 or v.get("relation") not in (None,) + MINOR_RELATIONS):
                return "a minor with adult facts"
    if pack == "safety" and v.get("days_off") is not None and v.get("hours_lost") is not None and \
            v["hours_lost"] < WORKDAY_HOURS * (v["days_off"] - 1):
        return "fewer working hours lost than the days off work imply"
    if f.get("opened") is not None and date_floor(f) > f["opened"]:
        return "a date fact after the file was opened"
    return None


# Pool syllable names that turned out to be real words found in JevBench public / OHS-1/2 text (SPEC 7.7 name check,
# yn2b/f6_precheck.py): never used by F6.
BLOCKED_NAMES = frozenset({"Solar"})


class SafePool:
    """mv_core.NamePool for one split, minus BLOCKED_NAMES (a blocked stem / first name / surname is redrawn)."""

    def __init__(self, pool: mv.NamePool):
        self.p = pool
        self.split = pool.split

    def _ok(self, s: str) -> bool:
        return not any(w in BLOCKED_NAMES for w in s.split())

    def _draw(self, fn, rng):
        for _ in range(100):
            x = fn(rng)
            if self._ok(x):
                return x
        raise SampleFail("name pool exhausted")

    def person(self, rng):
        return self._draw(self.p.person, rng)

    def org(self, rng):
        return self._draw(self.p.org, rng)

    def stem(self, rng):
        return self._draw(self.p.stem, rng)

    @staticmethod
    def ident(rng, prefix="W", digits=7):
        return mv.NamePool.ident(rng, prefix, digits)


# ------------------------------------------------------------------------------------------------ conditions + values
def make_cond(rng, a: dp.Attr) -> dict:
    if a.kind in ("num", "date"):
        return {"attr": a.id, "kind": a.kind, "op": rng.choice(OPS), "limit": rng.choice(a.limits)}
    if a.kind == "cat":
        k = rng.choice((1, 2, 2, 3))
        vs = sorted(rng.sample(a.values, k), key=a.values.index)
        return {"attr": a.id, "kind": "cat", "values": vs}
    return {"attr": a.id, "kind": "flag", "want": rng.random() < 0.6}


def _side(a: dp.Attr, c: dict, want: bool) -> tuple[int, int] | None:
    """The integer interval [x, y] of values of a for which cond c holds (want) or fails; None if empty."""
    lo, hi, L, op = a.lo, a.hi, c["limit"], c["op"]
    holds = {">=": (L, hi), ">": (L + 1, hi), "<=": (lo, L), "<": (lo, L - 1)}[op]
    fails = {">=": (lo, L - 1), ">": (lo, L), "<=": (L + 1, hi), "<": (L, hi)}[op]
    x, y = holds if want else fails
    x, y = max(x, lo), min(y, hi)
    return (x, y) if x <= y else None


def _readable(v: int, x: int, y: int, L: int) -> int:
    """Round a value far from the limit to a readable step, staying inside [x, y]."""
    span = y - x
    step = 1 if span <= 40 else (5 if span < 400 else (50 if span < 20000 else (1000 if span < 2_000_000 else 10000)))
    if step > 1 and abs(v - L) > 2 * step:
        v2 = v - (v % step)
        if x <= v2 <= y:
            return v2
    return v


def value_for(rng, a: dp.Attr, c: dict, want: bool, flavor: str = "any"):
    """A value of attribute a that makes cond c hold (want) or fail. flavor (num/date): at (exactly the limit), off1
    (one unit from the limit, on the wanted side), near (at or one unit off), far (at least 3 units away), any."""
    if a.kind in ("num", "date"):
        side = _side(a, c, want)
        if side is None:
            raise SampleFail("empty value range")
        x, y = side
        L = c["limit"]
        if flavor in ("at", "off1", "near"):
            ok = {"at": (0,), "off1": (1,), "near": (0, 1)}[flavor]
            xs = [v for v in (L - 1, L, L + 1) if x <= v <= y and abs(v - L) in ok]
            if not xs and flavor == "at":  # the limit is on the other side: one unit off is the closest boundary
                xs = [v for v in (L - 1, L + 1) if x <= v <= y]
            if not xs:
                raise SampleFail(f"no {flavor} value")
            return rng.choice(xs)
        if flavor == "far":
            xs = [(max(x, L + 3), y), (x, min(y, L - 3))]
            xs = [(p, q) for p, q in xs if p <= q]
            if xs:
                p, q = rng.choice(xs)
                return _readable(rng.randint(p, q), p, q, L)
        return _readable(rng.randint(x, y), x, y, L)
    if a.kind == "cat":
        pool = [v for v in a.values if (v in c["values"]) == want]
        if not pool:
            raise SampleFail("empty category pool")
        return rng.choice(pool)
    return c["want"] if want else (not c["want"])


def free_value(rng, a: dp.Attr):
    if a.kind in ("num", "date"):
        v = rng.randint(a.lo, a.hi)
        if a.kind == "num" and a.hi - a.lo > 400:
            v -= v % (50 if a.hi - a.lo < 20000 else 1000)
            v = max(a.lo, v)
        return v
    if a.kind == "cat":
        return rng.choice(a.values)
    return rng.random() < 0.5


# ------------------------------------------------------------------------------------------------ the item
def _flavor(rng, tier: str, role: str) -> str:
    """Boundary hard cases (SPEC 4.7): hard items put more values at or next to a limit."""
    p_at, p_off = {"easy": (0.04, 0.06), "standard": (0.12, 0.12), "judge": (0.12, 0.12),
                   "hard": (0.25, 0.2)}[tier]
    if role == "near":
        return "near"
    x = rng.random()
    return "at" if x < p_at else ("off1" if x < p_at + p_off else "far")


def sample(rng: random.Random, ctx: dict, pool: mv.NamePool) -> dict:
    """One fact pattern aimed at ctx (see the module docstring). Raises SampleFail when the target cannot be met."""
    pack, term = dp.term_of(ctx["gid"])
    tier, dk, truth = ctx["tier"], ctx["dk"], ctx["truth"]
    kn = TIER_KNOBS[tier]
    choice = ctx.get("choice", False)
    excg, miss = ctx.get("excg"), ctx.get("miss")
    joiner = "all" if choice or rng.random() < 0.62 else "any"
    n_el = rng.choice(kn["n_el"])
    n_ex = _wchoice(rng, kn["n_ex"])
    if dk in ("excl",) or excg in ("allow_deny", "deny_allow", "near_miss"):
        n_ex = max(1, n_ex)
    p_deem = kn["deem"] if truth else DEEM_FALSE[tier]
    want_deem = dk == "deem" or (not choice and dk not in ("rincl",) and rng.random() < p_deem)
    attrs = list(pack.attrs)
    pref = [a for a in attrs if a.id in term.prefer]
    rest = [a for a in attrs if a.id not in term.prefer]
    rng.shuffle(pref)
    rng.shuffle(rest)
    order_pool = pref + rest
    linked = {x: set(g) - {x} for g in dp.EXCLUSIVE_ATTRS.get(pack.id, ()) for x in g}

    def take(kind_pred=None):
        for i, a in enumerate(order_pool):
            if kind_pred is None or kind_pred(a):
                b = order_pool.pop(i)
                order_pool[:] = [x for x in order_pool if x.id not in linked.get(b.id, ())]
                return b
        raise SampleFail("attributes exhausted")

    # outside rule: any free attribute (its condition always holds for the item)
    els = [take() for _ in range(n_el)]
    exs = []
    for j in range(n_ex):
        numeric = excg == "near_miss" and j == 0
        exs.append(take((lambda a: a.kind in ("num", "date")) if numeric else None))
    unl = []
    for j in range(n_ex):
        need = (excg == "deny_allow" and j == 0) or (excg == "allow_deny" and j == 0 and rng.random() < 0.5) or \
               (rng.random() < kn["unless"])
        unl.append(take() if need and len(order_pool) > 2 else None)
    deem_a = take() if want_deem and len(order_pool) > 2 else None
    if dk == "deem" and deem_a is None:
        raise SampleFail("no attribute for the deeming clause")
    r_a = take()
    n_irr = rng.choice(kn["irrelevant"])
    irr = [take() for _ in range(min(n_irr, len(order_pool)))]
    if not irr and miss == "irrelevant":
        raise SampleFail("no irrelevant attribute")

    f = {"pack": pack.id, "term": ctx["gid"], "entity": pack.entity, "joiner": joiner,
         "elements": [make_cond(rng, a) for a in els],
         "exclusions": [{"trigger": make_cond(rng, a), "unless": make_cond(rng, u) if u else None}
                        for a, u in zip(exs, unl)],
         "deem": make_cond(rng, deem_a) if deem_a else None}
    r_eff = {"rincl": "incl", "rexcl": "excl"}.get(dk)
    if r_eff is None:
        # the outside rule's own verdict: incl = "it is a <term>", excl = "it is not"; r_agree steers it
        agree = ctx.get("r_agree", rng.random() < 0.5)
        r_eff = "incl" if (agree == truth) else "excl"
    f["outside"] = {"regime": rng.choice(pack.regimes), "cond": make_cond(rng, r_a), "effect": r_eff}
    f["r_card"] = dk in ("rincl", "rexcl")
    f["r_facts"] = ctx.get("r_place", "none") in ("facts", "both")
    if f["r_card"] and f["outside"]["effect"] == "incl" and f["deem"] is not None:
        f["deem"] = None
        deem_a = None
    vals = {}
    A = {a.id: a for a in pack.attrs}

    def setv(c, want, flavor="any"):
        vals[c["attr"]] = value_for(rng, A[c["attr"]], c, want, flavor)

    # ---- the outside rule always holds
    setv(f["outside"]["cond"], True, _flavor(rng, tier, "r"))
    # ---- elements
    el_truth = _element_plan(rng, joiner, n_el, dk, truth)
    miss_el = None
    if miss == "decisive" and dk == "elem":
        cand = [i for i, t in enumerate(el_truth) if not t]
        miss_el = rng.choice(cand)
    for i, (c, t) in enumerate(zip(f["elements"], el_truth)):
        if i == miss_el:
            vals[c["attr"]] = None
        else:
            setv(c, t, _flavor(rng, tier, "el"))
    # ---- deeming clause
    if f["deem"] is not None:
        setv(f["deem"], dk == "deem", _flavor(rng, tier, "deem"))
    # ---- exclusions
    applying = 0 if dk == "excl" else None
    miss_trig = miss_unless = None
    if miss == "decisive" and truth and f["exclusions"] and excg is None:
        miss_trig = rng.randrange(len(f["exclusions"]))
    if miss == "decisive" and not truth and dk == "excl" and f["exclusions"][0]["unless"] is not None:
        miss_unless = 0
    for j, x in enumerate(f["exclusions"]):
        trig, unless = x["trigger"], x["unless"]
        if j == applying:
            setv(trig, True, _flavor(rng, tier, "ex"))
            if unless is not None:
                if j == miss_unless:
                    vals[unless["attr"]] = None
                else:
                    setv(unless, False, _flavor(rng, tier, "un"))
            continue
        if j == miss_trig:
            vals[trig["attr"]] = None
            if unless is not None:
                vals[unless["attr"]] = free_value(rng, A[unless["attr"]])
            continue
        mode = "false"
        if j == 0 and excg == "deny_allow" and unless is not None:
            mode = "rescued"
        elif j == 0 and excg == "near_miss":
            mode = "near"
        if mode == "rescued":
            setv(trig, True, _flavor(rng, tier, "ex"))
            setv(unless, True, _flavor(rng, tier, "un"))
        elif mode == "near":
            if trig["kind"] not in ("num", "date"):
                raise SampleFail("near miss needs a numeric trigger")
            setv(trig, False, "near")
            if unless is not None:
                vals[unless["attr"]] = free_value(rng, A[unless["attr"]])
        else:
            setv(trig, False, "far")
            if unless is not None:
                vals[unless["attr"]] = free_value(rng, A[unless["attr"]])
    # ---- irrelevant attributes
    for j, a in enumerate(irr):
        vals[a.id] = None if (miss == "irrelevant" and j == 0) else free_value(rng, a)
    # ---- display order: definition attributes and irrelevant ones mixed
    shown = [c["attr"] for c in f["elements"]] + [x["trigger"]["attr"] for x in f["exclusions"]] + \
            [x["unless"]["attr"] for x in f["exclusions"] if x["unless"]] + \
            ([f["deem"]["attr"]] if f["deem"] else []) + [f["outside"]["cond"]["attr"]] + [a.id for a in irr]
    rng.shuffle(shown)
    f["order"] = shown
    f["values"] = vals
    # ---- names, usage, background
    f.update(_names(rng, pack, term, pool, ctx, truth))
    f["opened"] = opened_day(f, f["opened"])
    f["notes"] = [f"File opened by {f['officer']} on {dp.fmt_date(dp.day(f['opened']))}."]
    why = incoherent(f)
    if why:
        raise SampleFail(why)
    ev = dc.evaluate(f)
    if ev["truth"] != truth or not ev["unique"]:
        raise SampleFail("target missed")
    if choice and dc.failing_condition(f, ev) is None:
        raise SampleFail("no unique failing condition")
    if dc.exc_group(f) != (f"exc:{excg}" if excg else None):
        raise SampleFail("exception group missed")
    if dc.missing_tag(f) != (f"missing_info:{miss}" if miss else None):
        raise SampleFail("missing-info target missed")
    return f


def _wchoice(rng, w: dict):
    x = rng.random() * sum(w.values())
    for k, v in w.items():
        x -= v
        if x <= 0:
            return k
    return k


def _element_plan(rng, joiner: str, n: int, dk: str, truth: bool) -> list[bool]:
    """Truth of each element: the element path holds exactly once for path / excl / rexcl items, fails otherwise
    (exactly one failing element under AND, so that every reason is unique)."""
    path = dk in ("path", "excl", "rexcl")
    if joiner == "all":
        if path:
            return [True] * n
        out = [True] * n
        out[rng.randrange(n)] = False
        return out
    if path:
        out = [False] * n
        out[rng.randrange(n)] = True
        return out
    return [False] * n


def _names(rng, pack: dp.Pack, term: dp.Term, pool: mv.NamePool, ctx: dict, truth: bool) -> dict:
    """Item, file and the everyday-usage statement (its verdict = truth when usage_agree)."""
    W = truth if ctx.get("usage_agree", rng.random() < 0.5) else (not truth)
    at = dp.a_term(term)
    field_t, _, src = dp.DESC[pack.id]
    name, org = pool.person(rng), pool.org(rng)
    if src == "goods":
        if term.items:
            cands = [(it, s) for it, us in term.items for s, v in us if v == W]
            if not cands:
                raise SampleFail("no usage statement with that verdict")
            item, stmt = rng.choice(cands)
        else:
            item = rng.choice(pack.items)
            stmt = next(s for s, v in pack.usage if v == W).format(item=item, t=term.name, at=at)
    else:
        item = name if src == "person" else org
        stmt = next(s for s, v in pack.usage if v == W).format(item=item, t=term.name, at=at)
    desc = field_t.format(item=item, org=org, name=name)
    officer = pool.person(rng)
    bg_from = pool.person(rng)
    while bg_from == officer:
        bg_from = pool.person(rng)
    in_force = in_force_day(pack, rng.randint(1, 45))
    opened = rng.randint(60, 335)          # moved after every date fact by sample() (opened_day)
    n_neutral = rng.choice(TIER_KNOBS[ctx["tier"]]["neutral"])
    bg_order = ["usage", "r"] + [f"n{k}" for k in range(len(pack.neutral))]
    rng.shuffle(bg_order)
    return {"item": item, "name": name, "org": org, "description": desc, "usage": {"text": stmt, "verdict": W},
            "officer": officer, "bg_from": bg_from, "ref": f"{pack.ref}-{rng.randint(100000, 999999)}",
            "clause_no": rng.randint(3, 48), "in_force": in_force, "opened": opened,
            "neutral": rng.sample(pack.neutral, n_neutral), "bg_order": bg_order,
            "notes": [f"File opened by {officer} on {dp.fmt_date(dp.day(opened))}."], "filler": [],
            "record": None}
