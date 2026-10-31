"""F3 gen3_state_track: the typed state machines, the event sampler and the simulator (yn2b/SPEC.md section 5 F3).

This module owns the LABELS of family F3. Every label is computed here by a deterministic program (`decide`), never by
a model. gen3_state_track.py turns worlds into rows (formats, views, balance) through golden_src/gen3/mv_core.py.

  World     one latent state-tracking item: starting state, typed events (each event, structured or language, maps
            to exactly one typed update), parameters stated in the rules (roster, admins, time zone, limits, ...), the
            query time, and optionally an agent record (judge rows).
  replay    applies the events in timestamp order under the machine's rules. `flags` switch on the named SHORTCUT
            solvers (SPEC F3 shortcuts), which are used for tiers, distractors and checks only, never for labels:
              ignore_guards        guard-failing events are applied anyway
              apply_resends_twice  a repeated event id takes effect again
              display_order        events are applied in the order they are LISTED in the rendered row
              ignore_expiry        holds, grants, authorisations, overrides and locks never expire
              fuzzy_entity_id      events on look-alike ids are applied to the id they imitate
              last_event_wins      the value named by the last event that names the entity (no replay)
  decide    (gold, trace) of one query on one world; UNDEFINED when the queried value is left open (rejected item).

Machines (SPEC F3): orders, tickets (business-hours SLA), access, inventory, bookings, ledger, dialogue (slots),
agent (tool calls on a cart or files, failed calls, partial batches); held out for dev: flags, docs.

Stdlib + mv_core only; CPU only; deterministic (all randomness comes from the rng passed in).
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from fractions import Fraction
from typing import Any
import zoneinfo

import mv_core as mv

UTC = timezone.utc
SHORTCUT_FLAGS = {"ignore_guards": "guards", "apply_resends_twice": "resend", "display_order": "display",
                  "ignore_expiry": "expiry", "fuzzy_entity_id": "fuzzy"}
SHORTCUT_NAMES = ("last_event_wins",) + tuple(SHORTCUT_FLAGS)
TRAIN_MACHINES = ("orders", "tickets", "access", "inventory", "bookings", "ledger", "dialogue", "agent")
HOLDOUT_MACHINES = ("flags", "docs")
ALL_MACHINES = TRAIN_MACHINES + HOLDOUT_MACHINES


# ================================================================================================ data types
@dataclass
class Ev:
    """One event line. idx = creation order (stable across twins); eid = the event / message / call id (a resend
    repeats it); ts = aware UTC time; src = the system or person that logged it; kind + ent + a = the typed update;
    style s (structured) | l (language); lt = which language template."""
    idx: int
    eid: str
    ts: datetime
    src: str
    kind: str
    ent: str | None
    a: dict = field(default_factory=dict)
    style: str = "s"
    lt: int = 0
    resend: bool = False


@dataclass
class World:
    machine: str
    t0: datetime                   # time of the starting state
    t_end: datetime                # log export time
    t_q: datetime                  # query time (== t_end when at_end)
    at_end: bool
    ents: dict                     # listed id -> initial fields
    target: str
    decoys: dict                   # look-alike id -> the id it imitates (listed or not)
    events: list
    params: dict
    title: str
    notes: list
    offsets: dict                  # src -> UTC offset in minutes used when that source's times are printed
    ts_style: str
    rule_dates: list = field(default_factory=list)
    record: list | None = None     # judge: [(obs key, recorded value)]
    tags: set = field(default_factory=set)

    def copy(self) -> "World":
        return copy.deepcopy(self)


@dataclass
class Query:
    """What a row asks. qtype value | yn | score | judge; fam = the machine's query family; key = the observable;
    arg = the named value / threshold of a yes/no predicate; keys = the observables a count runs over."""
    qtype: str
    fam: str
    key: tuple | None = None
    arg: Any = None
    keys: tuple = ()


class Spec:
    """Sampling plan of one world: tier, number of events, trap counts, query time mode, language share."""

    def __init__(self, tier, n_events, traps, at_end=True, lang=0.5, mixed=False, qtype="yn", n_ent=None):
        self.tier, self.n_events, self.traps, self.at_end = tier, n_events, dict(traps), at_end
        self.lang, self.mixed, self.qtype, self.n_ent = lang, mixed, qtype, n_ent


# ================================================================================================ helpers
def ident(rng, prefix: str, digits: int, used: set) -> str:
    for _ in range(200):
        body = "".join(rng.choice("0123456789") for _ in range(digits))
        s = prefix + body
        if s not in used and body[0] != "0" and any(body[i] != body[i + 1] for i in range(len(body) - 1)):
            used.add(s)
            return s
    raise mv.Reject("ident")


def decoy_of(rng, s: str, used: set) -> str:
    for _ in range(30):
        d = mv.decoy_id(s, rng)
        if d not in used:
            used.add(d)
            return d
    raise mv.Reject("decoy")


def pick(rng, xs):
    xs = list(xs)
    return xs[rng.randrange(len(xs))] if xs else None


def money(c: int, cur: str | None = None) -> str:
    s = mv.fmt_amount(Fraction(c, 100), 2)
    return f"{s} {cur}" if cur else s


def when_text(W: World, end_phrase: str = "at the end of the log") -> str:
    return end_phrase if W.at_end else f"at {mv.fmt_ts(W.t_q.astimezone(UTC), 'iso')}"


def _undo(st: dict, recs: list) -> None:
    for r in reversed(recs):
        op = r[0]
        if op == "set":
            st[r[1]][r[2]] = r[3]
        elif op == "add":
            st[r[1]][r[2]] -= r[3]
        elif op == "pop":
            st[r[1]][r[2]].pop(r[3], None)
        elif op == "put":
            st[r[1]][r[2]][r[3]] = r[4]
        elif op == "gset":
            st["_"][r[1]] = r[2]
        elif op == "popv":
            st[r[1]]["vers"].pop()
        elif op == "sub0":
            st[r[1]][r[2]] = max(0, st[r[1]][r[2]] - r[3])
        else:
            raise ValueError(op)


# ================================================================================================ machine base
class Machine:
    name = ""
    noun = ""
    plural = ""
    end_phrase = "at the end of the log"
    has_expiry = False
    has_revert = True
    gap = (3, 95)
    ent_digits = 7
    ent_prefix = ""
    TXT: dict = {}
    SRC: dict = {}
    VALUE_TPL: dict = {}
    SCORE_TPL: dict = {}
    YN: dict = {}          # fam -> {"q": {tpl: text}, "neg": {tpl: text}, "card": {...}, "ncard": {...}, "jb": (y, n)}

    # ---------------------------------------------------------------- to implement
    def new_world(self, rng, pool, spec: Spec) -> World: ...

    def init(self, W: World) -> dict: ...

    def apply(self, st, e: Ev, ent, W: World, flags) -> list | str: ...

    def moves(self, st, W: World, ent, t, rng, mode: str) -> list: ...

    def observe(self, st, W: World, flags) -> dict: ...

    def rules(self, W: World) -> list[str]: ...

    def start_rows(self, W: World) -> list: ...

    def context(self, W: World) -> list: ...

    def label(self, key: tuple, W: World) -> str: ...  # 'order SO-4417203 status'

    def vtext(self, key: tuple, v, W: World) -> str: ...  # option / record text of an observable value

    def queries(self, W: World, qtype: str, rng) -> list[Query]: ...

    def last_event(self, W: World, key: tuple): return None

    def expiring(self, W: World) -> bool: return False

    # ---------------------------------------------------------------- shared
    def revert_ok(self, st, e, W) -> bool:
        return True

    def text(self, e: Ev, W: World) -> str:
        s, ls = self.TXT[e.kind]
        f = dict(e.a)
        f["e"] = e.ent
        f.update(self.text_fields(e, W))
        tpl = s if e.style == "s" or not ls else ls[e.lt % len(ls)]
        return tpl.format(**f)

    def text_fields(self, e, W) -> dict:
        return {}

    def when(self, W) -> str:
        return when_text(W, self.end_phrase)

    rule_style = "a"  # the held-out machines use their own wording ("b") of the common rules (SPEC 6 holdout phrasings)

    def common_rules(self, W, revert=True, request=True) -> list[str]:
        if self.rule_style == "b":
            out = ["Every line in the log asks for one change. If that change breaks a rule at the time it is asked "
                   "for, it is refused and nothing changes."] if request else []
            out += ["Changes apply in the order of their timestamps, not the order the lines appear in. Convert any "
                    "time that carries a UTC offset to UTC before comparing.",
                    "An event id can apply only once. If the same id shows up again after it already applied, the "
                    "repeat is ignored.",
                    f"The {self.plural} in the starting state are the only ones that exist. A line about any other id "
                    f"is ignored, even if it differs by only a character or two; ids have to match exactly.",
                    "For a question about a given time, only lines timestamped at or before that time count."]
            if revert and self.has_revert:
                out.append("A revert names an earlier event id. If that event applied and was not reverted before, "
                           "the values it changed return to what they were right before it; otherwise the revert "
                           "does nothing.")
            return out
        out = []
        if request:
            out.append("Each event line is a request. A request that breaks a rule at the moment it happens is "
                       "rejected and changes nothing.")
        out += ["Events take effect in timestamp order, whatever order they are listed in. Times written with a UTC "
                "offset are converted to UTC before they are compared.",
                "Each event id takes effect at most once. A later line that repeats an id that already took effect is "
                "a redelivery and changes nothing.",
                f"Only the {self.plural} listed in the starting state exist. An event that names any other id changes "
                f"nothing, even when the id looks almost the same: ids must match character for character.",
                "The state at a stated time counts only the events timestamped at or before that time."]
        if revert and self.has_revert:
            out.append(self.revert_rule)
        return out

    revert_rule = ("A revert line names an earlier event id. If that event took effect and has not been reverted yet, "
                   "every value it changed goes back to what it was just before that event; otherwise the revert "
                   "changes nothing.")

    def other_ent(self, W: World, rng):
        """The entity of an 'other' slot: a listed entity that is neither the queried one nor a look-alike."""
        others = [x for x in W.ents if x != W.target and x not in W.decoys] or \
                 [x for x in W.ents if x != W.target] or [W.target]
        return pick(rng, others)

    def mentions(self, e: Ev) -> set:
        """Every entity id an event line names."""
        return {e.ent}

    def guard_present(self, W: World, out: dict) -> bool:
        """Is a guard-failing request (before the query time) in the log?"""
        return any(out[e.idx] == "guard" for e in W.events if e.ts <= W.t_q)

    def mix_offsets(self, W: World, rng, spec) -> None:
        if spec.mixed:
            for s_ in sorted(W.offsets):
                W.offsets[s_] = rng.choice([0, 60, 120, -300, -240, 330, 540, 0])

    def gapmin(self, rng) -> int:
        return rng.randint(*self.gap)

    def ent_ids(self, rng, n, used):
        return [ident(rng, self.ent_prefix, self.ent_digits, used) for _ in range(n)]

    def add_decoy(self, rng, W: World, used: set, listed: bool, init_fields: dict | None = None):
        d = decoy_of(rng, W.target, used)
        W.decoys[d] = W.target
        if listed:
            W.ents[d] = dict(init_fields if init_fields is not None else W.ents[W.target])
        return d


# ================================================================================================ replay + sampler
def step(M: Machine, W: World, st, took: dict, reverted: set, e: Ev, flags=frozenset()):
    """Apply one event; returns 'ok' | 'dup' | 'unknown' | 'guard'."""
    if e.eid in took and "resend" not in flags:
        return "dup"
    ent = W.decoys.get(e.ent, e.ent) if "fuzzy" in flags else e.ent
    if e.kind == "revert":
        of = e.a["of"]
        if of in took and of not in reverted and ("guards" in flags or M.revert_ok(st, e, W)):
            _undo(st, took[of])
            reverted.add(of)
            took.setdefault(e.eid, [])
            return "ok"
        return "guard"
    u = M.apply(st, e, ent, W, flags)
    if isinstance(u, str):
        return u
    took.setdefault(e.eid, u)
    return "ok"


def time_order(W: World) -> list:
    return sorted(W.events, key=lambda e: (e.ts, e.idx))


def replay(M: Machine, W: World, flags=frozenset(), display: list | None = None):
    """Final state at W.t_q and the per-event outcome {idx: ok|dup|unknown|guard|after}."""
    st = M.init(W)
    seq = [W.events[i] for i in display] if ("display" in flags and display is not None) else time_order(W)
    took, rev, out = {}, set(), {}
    for e in seq:
        if e.ts > W.t_q:
            out[e.idx] = "after"
            continue
        out[e.idx] = step(M, W, st, took, rev, e, flags)
    return st, out


def observe(M: Machine, W: World, flags=frozenset(), display=None) -> dict:
    st, _ = replay(M, W, flags, display)
    return M.observe(st, W, flags)


def answer(M: Machine, W: World, q: Query, obs: dict):
    """The answer of query q given observables (truth or a shortcut's): value -> option text; yn/judge -> 'yes'/'no';
    score -> level index. UNDEFINED when the value is open or the observable is missing."""
    if q.qtype == "judge":
        if not W.record:
            return mv.UNDEFINED
        for k, v in W.record:
            if k not in obs or obs[k] is None:
                return mv.UNDEFINED
        return "yes" if all(obs[k] == v for k, v in W.record) else "no"
    if q.qtype == "score":
        return M.level(W, q, obs)
    if q.key not in obs or obs[q.key] is None:
        return mv.UNDEFINED
    v = obs[q.key]
    if q.qtype == "value":
        return v
    return "yes" if M.pred(W, q, v) else "no"


def decide(M: Machine, W: World, q: Query):
    """(gold, trace) for query q on world W. gold: value (raw observable value), 'yes'/'no', or a level index;
    UNDEFINED when the queried value is left open. trace: the decisive surface facts (target id and the id of the
    last event that changed the queried entity) plus the outcome of every event."""
    st, out = replay(M, W)
    obs = M.observe(st, W, frozenset())
    g = answer(M, W, q, obs)
    ent = W.target
    last = None
    for e in time_order(W):
        if out.get(e.idx) == "ok" and e.ent == ent:
            last = e.eid
    trace = {"outcome": out, "decisive": [ent] + ([last] if last else []), "obs": obs}
    return g, trace


def shortcut_answer(M: Machine, W: World, q: Query, name: str, display: list, in_play: dict):
    """The named shortcut solver's answer (None = the shortcut's trap is absent from this row, so it abstains)."""
    if not in_play.get(name):
        return None
    if name == "last_event_wins":
        if q.qtype in ("value", "yn", "judge"):
            obs = dict(observe(M, W))
            keys = [q.key] if q.qtype != "judge" else [k for k, _ in W.record]
            any_set = False
            for k in keys:
                v = M.last_event(W, k)
                if v is not None:
                    obs[k] = v
                    any_set = True
            if not any_set:
                return None
            a = answer(M, W, q, obs)
            return None if mv.is_undefined(a) else a
        return None
    obs = observe(M, W, frozenset({SHORTCUT_FLAGS[name]}), display)
    a = answer(M, W, q, obs)
    return None if mv.is_undefined(a) else a


def in_play(M: Machine, W: World, display: list) -> dict:
    """Which shortcut traps are present in the row (surface presence, not effect): a guard-failing event, a
    redelivered id, a listing order that differs from time order, an expiring object, an event on a look-alike id,
    or 2+ events naming the queried entity (last_event_wins)."""
    _, out = replay(M, W)
    pre = [e for e in W.events if e.ts <= W.t_q]
    chrono = [e.idx for e in time_order(W)]
    return {"ignore_guards": M.guard_present(W, out),
            "apply_resends_twice": any(out[e.idx] == "dup" for e in pre),
            "display_order": display is not None and list(display) != chrono,
            "ignore_expiry": M.expiring(W),
            "fuzzy_entity_id": any(M.mentions(e) & set(W.decoys) for e in pre),
            "last_event_wins": sum(1 for e in pre if W.target in M.mentions(e)) >= 2}


def sample_world(M: Machine, rng, pool, spec: Spec) -> World:
    """Build one world: entities from the machine, then events slot by slot (valid moves on the queried entity, other
    entities, guard-failing requests, redeliveries, reverts, look-alike-id events, short-lived expiring objects and
    events after the query time), simulating as it goes so every slot has the outcome it was meant to have."""
    W = M.new_world(rng, pool, spec)
    n = spec.n_events
    traps = []
    for k, c in sorted(spec.traps.items()):
        if k != "after":
            traps += [k] * c
    n_after = spec.traps.get("after", 0) if not spec.at_end else 0
    rest = max(0, n - len(traps) - n_after)
    n_main = max(1, round(rest * 0.5))
    slots = traps + ["main"] * n_main + ["other"] * max(0, rest - n_main)
    rng.shuffle(slots)
    first_main = next((i for i, s in enumerate(slots) if s == "main"), 0)
    if first_main:
        slots.insert(0, slots.pop(first_main))
    for k in ("resend", "revert"):  # redeliveries and reverts need an earlier applied event: push them back
        if k in slots[:2] and len(slots) > 2:
            i = slots.index(k)
            slots.append(slots.pop(i))
    slots += ["after"] * n_after
    st = M.init(W)
    took, rev = {}, set()
    evs: list[Ev] = []
    used_eids: set = set()
    t = W.t0
    applied_target = []
    after_idx: set = set()
    def effective(ev, flag):
        """Would the shortcut that mishandles this trap (applying a redelivery again, a guard-failing request anyway,
        or a look-alike-id event to the id it imitates) change an observable now? Traps that matter are preferred."""
        if flag is None:
            return False
        old_tq = W.t_q
        W.t_q = t
        try:
            before = M.observe(st, W, frozenset())
            st2 = copy.deepcopy(st)
            res = step(M, W, st2, dict(took), set(rev), ev, frozenset({flag}))
            return res == "ok" and M.observe(st2, W, frozenset()) != before
        except (KeyError, ValueError, TypeError, IndexError):
            return False
        finally:
            W.t_q = old_tq

    def prefer(cands, flag):
        eff = [c for c in cands if effective(c, flag)]
        return eff if (eff and rng.random() < 0.85) else cands

    for slot in slots:
        t = t + timedelta(minutes=M.gapmin(rng) + (3 if slot == "after" and not after_idx else 0))
        e = None
        if slot == "resend":
            cands = [x for x in evs if not x.resend and took.get(x.eid) is not None and x.kind != "revert"]
            tc = [x for x in cands if x.ent == W.target] or cands
            tc = [Ev(len(evs), x.eid, t, x.src, x.kind, x.ent, dict(x.a), x.style, x.lt, True) for x in tc]
            e = pick(rng, prefer(tc, "resend"))
        elif slot == "revert" and M.has_revert:
            cands = [x for x in evs if x.ent == W.target and x.eid in took and x.eid not in rev and x.kind != "revert"
                     and not x.resend]
            src = pick(rng, cands)
            if src is not None:
                e = Ev(len(evs), M.new_eid(rng, used_eids), t, M.SRC.get("revert", "ops-console"), "revert",
                       src.ent, {"of": src.eid}, M.style(rng, spec), rng.randrange(4))
        if e is None and slot not in ("resend", "revert"):
            mode = slot
            if slot == "decoy":
                if not W.decoys:
                    mode = "other"
            ent = W.target if mode in ("main", "guard", "expiry", "after") else None
            if mode == "decoy":
                ent = pick(rng, sorted(W.decoys))
            elif mode == "other":
                ent = M.other_ent(W, rng)
            cands = M.moves(st, W, ent, t, rng, mode)
            if not cands and mode in ("guard", "expiry", "decoy"):
                cands = M.moves(st, W, W.target, t, rng, "main")
                ent = W.target
            if not cands and mode != "main":
                cands = M.moves(st, W, W.target, t, rng, "main")
                ent = W.target
            if cands:
                evc = []
                for kind, a, src in cands:
                    a = dict(a)
                    evc.append(Ev(len(evs), "", t, src, kind, a.pop("_ent", ent), a, M.style(rng, spec),
                                  rng.randrange(4)))
                flag = {"guard": "guards", "decoy": "fuzzy"}.get(mode)
                e = pick(rng, prefer(evc, flag) if flag else evc)
                e.eid = M.new_eid(rng, used_eids)
        if e is None:
            continue
        if slot == "after":
            after_idx.add(e.idx)
            evs.append(e)
            continue
        res = step(M, W, st, took, rev, e)
        if res == "ok" and e.ent == W.target:
            applied_target.append(e)
        evs.append(e)
    W.events = evs
    after = [e for e in evs if e.idx in after_idx]
    if after:
        last_pre = max((e.ts for e in evs if e.idx not in after_idx), default=W.t0)
        first_after = min(e.ts for e in after)
        span = int((first_after - last_pre).total_seconds() // 60)
        if span < 2:
            raise mv.Reject("sample", "no room for the query time")
        W.t_q = last_pre + timedelta(minutes=rng.randint(1, span - 1))
        W.at_end = False
        W.t_end = max(e.ts for e in evs) + timedelta(minutes=rng.randint(3, 40))
    else:
        W.t_end = max((e.ts for e in evs), default=W.t0) + timedelta(minutes=rng.randint(3, 40))
        W.t_q = W.t_end
        W.at_end = True
    M.finish(W, rng)
    return W


def _style(rng, spec):
    return "l" if rng.random() < spec.lang else "s"


Machine.style = staticmethod(_style)


def _new_eid(self, rng, used):
    return ident(rng, "E", 4, used)


Machine.new_eid = _new_eid
Machine.finish = lambda self, W, rng: None


def base_world(M: Machine, rng, pool, spec: Spec, ents: dict, target: str) -> World:
    day = date(2026, 1, 5) + timedelta(days=rng.randrange(0, 320))
    t0 = datetime(day.year, day.month, day.day, rng.randint(6, 14), rng.choice([0, 10, 20, 30, 40, 50]), tzinfo=UTC)
    srcs = sorted(set(M.SRC.values()))
    offs = {s: 0 for s in srcs}
    if spec.mixed:
        for s in srcs:
            offs[s] = rng.choice([0, 60, 120, -300, -240, 330, 540, 0])
    W = World(M.name, t0, t0, t0, True, ents, target, {}, [], {}, "", [], offs, rng.choice(["iso", "space"]))
    W.rule_dates = [t0.date() - timedelta(days=rng.randint(20, 400)) for _ in range(16)]
    W.title = M.make_title(rng, pool)
    return W


Machine.make_title = lambda self, rng, pool: f"{pool.org(rng)} - {self.noun} event log"


# ================================================================================================ F3.1 orders
class Orders(Machine):
    name, noun, plural, ent_prefix = "orders", "order", "orders", "SO-"
    gap = (5, 240)
    ST = ("created", "paid", "packed", "shipped", "delivered", "cancelled", "returned")
    MOVES = {"pay": (("created",), "paid"), "pack": (("paid",), "packed"), "ship": (("packed",), "shipped"),
             "deliver": (("shipped",), "delivered"), "cancel": (("created", "paid", "packed"), "cancelled"),
             "return": (("delivered",), "returned")}
    SRC = {"pay": "payments", "pack": "warehouse", "ship": "carrier-api", "deliver": "carrier-api",
           "cancel": "support-desk", "return": "returns-desk", "revert": "ops-console"}
    TXT = {"pay": ("pay order={e}", ("Payment captured for order {e}.", "Order {e}: the card payment went through.")),
           "pack": ("pack order={e}", ("Warehouse finished packing order {e}.", "Order {e} is boxed and labelled.")),
           "ship": ("ship order={e}", ("Carrier collected order {e}.", "Order {e} was handed to the courier.")),
           "deliver": ("deliver order={e}", ("Courier reports order {e} delivered.",
                                             "Order {e} reached the customer.")),
           "cancel": ("cancel order={e}", ("Cancellation requested for order {e}.",
                                           "Customer asked to cancel order {e}.")),
           "return": ("return order={e}", ("Returned parcel for order {e} checked in.",
                                           "Order {e} came back as a return.")),
           "revert": ("revert event={of}", ("Operator reverted event {of}.", "Undo of event {of} requested."))}
    DEFS = {"created": "the order exists and no payment has taken effect",
            "paid": "a payment took effect and the order is not packed yet",
            "packed": "the order is packed and has not left with a carrier",
            "shipped": "a carrier collected the order and delivery has not taken effect",
            "delivered": "delivery took effect and no return has",
            "cancelled": "a cancellation took effect",
            "returned": "a return took effect after delivery"}
    CANCELLABLE = ("created", "paid", "packed")
    SHIPPED = ("shipped", "delivered")

    def new_world(self, rng, pool, spec):
        used = set()
        # an order allows at most 5 steps, so long logs need more orders to stay within the tier's event range
        n = spec.n_ent or max(rng.randint(2, 4), min(8, spec.n_events // 4 + 1))
        ids = self.ent_ids(rng, n, used)
        ents = {}
        for i, x in enumerate(ids):
            s = rng.choice(["created", "created", "paid"]) if i == 0 else rng.choice(
                ["created", "paid", "packed", "shipped"] if spec.n_events < 13 else ["created", "created", "paid"])
            ents[x] = {"status": s, "customer": pool.person(rng)}
        W = base_world(self, rng, pool, spec, ents, ids[0])
        if spec.traps.get("decoy"):
            self.add_decoy(rng, W, used, rng.random() < 0.6,
                           {"status": rng.choice(["created", "paid"]), "customer": pool.person(rng)})
        return W

    def init(self, W):
        return {k: {"status": v["status"]} for k, v in W.ents.items()}

    def apply(self, st, e, ent, W, flags):
        if ent not in st:
            return "unknown"
        frm, to = self.MOVES[e.kind]
        cur = st[ent]["status"]
        if cur not in frm and "guards" not in flags:
            return "guard"
        st[ent]["status"] = to
        return [("set", ent, "status", cur)]

    def moves(self, st, W, ent, t, rng, mode):
        if ent not in st:
            return [(k, {}, self.SRC[k]) for k in self.MOVES]
        cur = st[ent]["status"]
        ok = [k for k, (frm, _) in self.MOVES.items() if cur in frm]
        bad = [k for k, (frm, _) in self.MOVES.items() if cur not in frm]
        if mode == "guard":
            return [(k, {}, self.SRC[k]) for k in bad]
        if mode == "main" and "cancel" in ok and len(ok) > 1 and rng.random() < 0.7:
            ok.remove("cancel")
        return [(k, {}, self.SRC[k]) for k in ok]

    def observe(self, st, W, flags):
        return {("status", k): st[k]["status"] for k in W.ents}

    def rules(self, W):
        return (["Order statuses change only by these steps: pay (created to paid), pack (paid to packed), ship "
                 "(packed to shipped), deliver (shipped to delivered), cancel (created, paid or packed to cancelled), "
                 "return (delivered to returned).",
                 "Language lines map to steps: a payment line is pay, a packing line is pack, a carrier or courier "
                 "collection line is ship, a delivery line is deliver, a cancellation line is cancel, a returned "
                 "parcel line is return, and an undo or revert line is a revert."]
                + self.common_rules(W))

    def start_rows(self, W):
        return [(k, [("status", v["status"]), ("customer", v["customer"])]) for k, v in W.ents.items()]

    def context(self, W):
        return [("system", "order desk"), ("orders tracked", str(len(W.ents)))]

    def label(self, key, W):
        return f"order {key[1]} status"

    def vtext(self, key, v, W):
        return v

    def last_event(self, W, key):
        v = None
        for e in time_order(W):
            if e.ts <= W.t_q and e.ent == key[1] and e.kind in self.MOVES:
                v = self.MOVES[e.kind][1]
        return v

    def domain(self, W, q):
        return list(self.ST)

    def option_defs(self, q, opts):
        return {o: self.DEFS[o] for o in sorted(opts) if o in self.DEFS}

    VALUE_TPL = {"ord.v.a": "What status does order {e} have {when}, under the numbered rules?",
                 "ord.v.b": "Under the order rules, which status is order {e} in {when}?"}
    SCORE_TPL = {"ord.sc.a": "How many of the listed orders are shipped or delivered {when}?",
                 "ord.sc.b": "Under the rules, how many listed orders have status shipped or delivered {when}?"}
    YN = {"eq": {"q": {"ord.eq.a": "Is order {e} in status {s} {when}?",
                       "ord.eq.b": "Under the numbered rules, is the status of order {e} {s} {when}?"},
                 "neg": {"ord.eqn.a": "Is order {e} in any status other than {s} {when}?"},
                 "card": {"yes": "Replaying the log under the numbered rules, the order named in the question has "
                                 "exactly the named status at the stated time.",
                          "no": "Under the rules that order has a different status at the stated time."},
                 "ncard": {"yes": "Under the rules the order named in the question has a status other than the named "
                                  "one at the stated time.",
                           "no": "Replaying the log under the rules, that order has exactly the named status then."},
                 "jb": ("Order {e} is in status {s} {when}.", "Order {e} is not in status {s} {when}.")},
          "cancel": {"q": {"ord.cx.a": "Can order {e} still be cancelled {when}?",
                           "ord.cx.b": "Under the rules, would a cancellation request for order {e} be allowed {when}?"},
                     "neg": {"ord.cxn.a": "Would a cancellation request for order {e} be rejected {when}?"},
                     "card": {"yes": "At the stated time the order is created, paid or packed, so a cancellation "
                                     "request then would take effect.",
                              "no": "At the stated time the order is shipped, delivered, cancelled or returned, so a "
                                    "cancellation request then would be rejected."},
                     "ncard": {"yes": "At the stated time the order is shipped, delivered, cancelled or returned, so "
                                      "a cancellation request would be rejected.",
                               "no": "At the stated time the order is created, paid or packed, so a cancellation "
                                     "request would take effect."},
                     "jb": ("Order {e} can still be cancelled {when}.", "Order {e} can no longer be cancelled {when}.")}}

    def queries(self, W, qtype, rng):
        k = ("status", W.target)
        if qtype == "value" or qtype == "judge":
            return [Query(qtype, "status", k)]
        if qtype == "yn":
            return [Query("yn", "eq", k), Query("yn", "cancel", k)]
        return [Query("score", "shipped", None, None, tuple(("status", x) for x in W.ents))]

    def pred(self, W, q, v):
        return v == q.arg if q.fam == "eq" else v in self.CANCELLABLE

    def levels(self, W, q):
        n = len(q.keys)
        return [f"{i} of the {n} listed orders" if i else f"none of the {n} listed orders" for i in range(n + 1)]

    def level(self, W, q, obs):
        return sum(1 for k in q.keys if obs.get(k) in self.SHIPPED)

    def qfields(self, W, q):
        return {"e": W.target, "s": q.arg}


# ================================================================================================ F3.2 tickets
class Tickets(Machine):
    name, noun, plural, ent_prefix, ent_digits = "tickets", "ticket", "tickets", "TCK-", 6
    gap = (20, 420)
    SRC = {"assign": "dispatch", "start": "agent-console", "wait": "agent-console", "resume": "mail-gateway",
           "resolve": "agent-console", "reopen": "mail-gateway", "close": "qa-bot", "revert": "ops-console"}
    MOVES = {"start": (("assigned",), "in_progress"), "wait": (("in_progress",), "waiting"),
             "resume": (("waiting",), "in_progress"), "resolve": (("in_progress", "waiting"), "resolved"),
             "reopen": (("resolved",), "in_progress"), "close": (("resolved",), "closed")}
    ASSIGNABLE = ("new", "assigned", "in_progress", "waiting")
    TXT = {"assign": ("assign ticket={e} owner={who}", ("Ticket {e} assigned to {who}.",
                                                        "{who} now owns ticket {e}.")),
           "start": ("start ticket={e}", ("Work started on ticket {e}.", "Ticket {e} picked up by its owner.")),
           "wait": ("wait ticket={e}", ("Ticket {e} is waiting on the customer.",
                                        "Asked the customer for details on ticket {e}.")),
           "resume": ("resume ticket={e}", ("Customer answered on ticket {e}.", "New customer message on ticket {e}.")),
           "resolve": ("resolve ticket={e}", ("Ticket {e} marked resolved.", "Fix confirmed for ticket {e}.")),
           "reopen": ("reopen ticket={e}", ("Customer reopened ticket {e}.", "Ticket {e} reopened.")),
           "close": ("close ticket={e}", ("Ticket {e} closed after review.", "Review done, ticket {e} closed.")),
           "revert": ("revert event={of}", ("Operator reverted event {of}.", "Undo of event {of} requested."))}
    STATUS_DEFS = {"new": "no owner assignment has taken effect", "assigned": "an owner is set and work has not "
                   "started", "in_progress": "the owner is working on it", "waiting": "waiting on the customer",
                   "resolved": "a resolution took effect and the ticket is not closed or reopened",
                   "closed": "closed after a resolution"}
    LEVELS = ("level 0 - not overdue", "level 1 - overdue by under 4 business hours",
              "level 2 - overdue by 4 to under 8 business hours", "level 3 - overdue by 8 to under 16 business hours",
              "level 4 - overdue by 16 business hours or more")
    ZONES = ("Europe/Berlin", "America/New_York", "Europe/London", "Asia/Singapore", "Australia/Sydney")

    def new_world(self, rng, pool, spec):
        used = set()
        n = spec.n_ent or rng.randint(2, 3)
        ids = self.ent_ids(rng, n, used)
        roster = sorted({pool.person(rng) for _ in range(3)})
        outsiders = sorted({pool.person(rng) for _ in range(2)} - set(roster))
        ents = {x: {"status": "new" if i == 0 else rng.choice(["new", "assigned"]), "owner": None} for i, x in
                enumerate(ids)}
        for x in ids[1:]:
            if ents[x]["status"] == "assigned":
                ents[x]["owner"] = rng.choice(roster)
        W = base_world(self, rng, pool, spec, ents, ids[0])
        zone = rng.choice(self.ZONES)
        # open the target inside business hours on a weekday
        for _ in range(60):
            day = W.t0.date() + timedelta(days=rng.randrange(0, 5))
            if day.weekday() < 5:
                break
        local = datetime(day.year, day.month, day.day, rng.randint(9, 15), rng.choice([0, 15, 30, 45]))
        opened = mv.to_utc(local, zone)
        W.t0 = opened
        hol = []
        if rng.random() < 0.5:
            d = day + timedelta(days=rng.randint(1, 3))
            if d.weekday() < 5:
                hol.append(d)
        W.params = {"roster": roster, "outsiders": outsiders, "zone": zone, "holidays": hol,
                    "sla": rng.choice([4, 8, 8, 16]), "opened": opened}
        if spec.traps.get("decoy"):
            self.add_decoy(rng, W, used, rng.random() < 0.6, {"status": "new", "owner": None})
        W.tags.add("hc:business_days")
        if hol:
            W.tags.add("hc:business_days")
        return W

    def init(self, W):
        return {k: {"status": v["status"], "owner": v["owner"], "res": None} for k, v in W.ents.items()}

    def apply(self, st, e, ent, W, flags):
        if ent not in st:
            return "unknown"
        s = st[ent]
        if e.kind == "assign":
            if ("guards" not in flags) and (s["status"] not in self.ASSIGNABLE or e.a["who"] not in W.params["roster"]):
                return "guard"
            u = [("set", ent, "owner", s["owner"]), ("set", ent, "status", s["status"])]
            s["owner"] = e.a["who"]
            if s["status"] == "new":
                s["status"] = "assigned"
            return u
        frm, to = self.MOVES[e.kind]
        if s["status"] not in frm and "guards" not in flags:
            return "guard"
        u = [("set", ent, "status", s["status"])]
        if e.kind == "resolve" and s["res"] is None:
            u.append(("set", ent, "res", None))
            s["res"] = e.ts
        s["status"] = to
        return u

    def moves(self, st, W, ent, t, rng, mode):
        R = W.params["roster"]
        if ent not in st:
            return [("assign", {"who": rng.choice(R)}, self.SRC["assign"]), ("resolve", {}, self.SRC["resolve"])]
        s = st[ent]
        out = []
        if mode == "guard":
            if s["status"] in self.ASSIGNABLE and W.params["outsiders"]:
                out.append(("assign", {"who": rng.choice(W.params["outsiders"])}, self.SRC["assign"]))
            out += [(k, {}, self.SRC[k]) for k, (frm, _) in self.MOVES.items() if s["status"] not in frm]
            return out
        if s["status"] in self.ASSIGNABLE:
            who = [p for p in R if p != s["owner"]]
            if who and (s["status"] == "new" or rng.random() < 0.5):
                out.append(("assign", {"who": rng.choice(who)}, self.SRC["assign"]))
        out += [(k, {}, self.SRC[k]) for k, (frm, _) in self.MOVES.items() if s["status"] in frm]
        if mode == "main" and s["status"] in ("in_progress", "waiting") and rng.random() < 0.4:
            out = [x for x in out if x[0] == "resolve"] or out
        return out

    # --- business hours
    def _windows(self, W, a, b):
        z = zoneinfo.ZoneInfo(W.params["zone"])
        d = a.astimezone(z).date() - timedelta(days=1)
        end = b.astimezone(z).date() + timedelta(days=1)
        while d <= end:
            if d.weekday() < 5 and d not in W.params["holidays"]:
                yield (mv.to_utc(datetime(d.year, d.month, d.day, 9, 0), W.params["zone"]),
                       mv.to_utc(datetime(d.year, d.month, d.day, 17, 0), W.params["zone"]))
            d += timedelta(days=1)

    def biz_minutes(self, W, a, b) -> int:
        if b <= a:
            return 0
        tot = 0
        for s, e in self._windows(W, a, b):
            lo, hi = max(a, s), min(b, e)
            if hi > lo:
                tot += int((hi - lo).total_seconds() // 60)
        return tot

    def due(self, W) -> datetime:
        need = W.params["sla"] * 60
        a = W.params["opened"]
        for s, e in self._windows(W, a, a + timedelta(days=30)):
            lo = max(a, s)
            if e <= lo:
                continue
            m = int((e - lo).total_seconds() // 60)
            if m >= need:
                return lo + timedelta(minutes=need)
            need -= m
        raise mv.Reject("sla_due")

    def observe(self, st, W, flags):
        out = {}
        for k in W.ents:
            out[("owner", k)] = st[k]["owner"] or "nobody"
            out[("status", k)] = st[k]["status"]
        s = st[W.target]
        due = self.due(W)
        res = s["res"]
        on_time = res is not None and res <= due
        overdue = (W.t_q > due) and not on_time
        late = self.biz_minutes(W, due, res if res is not None else W.t_q) if overdue else 0
        out[("overdue", W.target)] = overdue
        out[("level", W.target)] = 0 if not overdue else (1 if late < 240 else 2 if late < 480 else 3 if late < 960
                                                          else 4)
        return out

    def rules(self, W):
        p = W.params
        hol = ", ".join(d.isoformat() for d in p["holidays"]) or "none listed"
        return (["Ticket statuses: new, assigned, in_progress, waiting, resolved, closed. Steps: start (assigned to "
                 "in_progress), wait (in_progress to waiting), resume (waiting to in_progress, when the customer "
                 "answers), resolve (in_progress or waiting to resolved), reopen (resolved to in_progress), close "
                 "(resolved to closed).",
                 f"An assignment sets the owner and moves a new ticket to assigned. It is allowed only while the "
                 f"ticket is new, assigned, in_progress or waiting, and only to a person on the support roster: "
                 f"{', '.join(p['roster'])}.",
                 "Language lines map to steps: 'assigned to' or 'now owns' is an assignment, 'work started' or "
                 "'picked up' is start, 'waiting on the customer' or 'asked the customer' is wait, 'customer "
                 "answered' or 'new customer message' is resume, 'resolved' or 'fix confirmed' is resolve, "
                 "'reopened' is reopen, 'closed' is close, and an undo or revert line is a revert.",
                 f"Resolution is due {p['sla']} business hours after the ticket was opened. Business hours are "
                 f"09:00 to 17:00 local time in {p['zone']}, Monday to Friday, except these holidays: {hol}.",
                 "A ticket is on time if it first reached resolved at or before its due time; later reopening does "
                 "not change the first resolution time. It is overdue at a stated time if that time is after the due "
                 "time and it had not first reached resolved by the due time.",
                 "Escalation level at a stated time: level 0 if the ticket is not overdue; otherwise measure the "
                 "business time from the due time to its first resolution (or to the stated time, if it was not "
                 "resolved by then): under 4 business hours is level 1, 4 to under 8 is level 2, 8 to under 16 is "
                 "level 3, and 16 or more is level 4."]
                + self.common_rules(W))

    def start_rows(self, W):
        out = []
        for k, v in W.ents.items():
            row = [("status", v["status"]), ("owner", v["owner"] or "nobody")]
            if k == W.target:
                row.append(("opened", mv.fmt_ts(W.params["opened"], "iso")))
            out.append((k, row))
        return out

    def context(self, W):
        return [("system", "support desk"), ("sla clock zone", W.params["zone"])]

    def label(self, key, W):
        return {"owner": f"ticket {key[1]} owner", "status": f"ticket {key[1]} status",
                "overdue": f"ticket {key[1]} overdue", "level": f"ticket {key[1]} escalation level"}[key[0]]

    def vtext(self, key, v, W):
        if key[0] == "overdue":
            return "yes" if v else "no"
        if key[0] == "level":
            return self.LEVELS[v]
        return v

    def last_event(self, W, key):
        if key[0] not in ("owner", "status"):
            return None
        v = None
        for e in time_order(W):
            if e.ts <= W.t_q and e.ent == key[1]:
                if key[0] == "owner" and e.kind == "assign":
                    v = e.a["who"]
                elif key[0] == "status" and e.kind in self.MOVES:
                    v = self.MOVES[e.kind][1]
                elif key[0] == "status" and e.kind == "assign":
                    v = "assigned"
        return v

    def domain(self, W, q):
        if q.key[0] == "owner":
            return list(W.params["roster"]) + list(W.params["outsiders"]) + ["nobody"]
        return list(self.STATUS_DEFS)

    def option_defs(self, q, opts):
        if q.key[0] == "status":
            return {o: self.STATUS_DEFS[o] for o in sorted(opts) if o in self.STATUS_DEFS}
        return None

    VALUE_TPL = {"tck.v.a": "Who owns ticket {e} {when}, under the numbered rules?",
                 "tck.v.b": "Under the support rules, which person is the owner of ticket {e} {when}?"}
    SCORE_TPL = {"tck.sc.a": "What escalation level does ticket {e} have {when}?",
                 "tck.sc.b": "Under the SLA rules, which escalation level applies to ticket {e} {when}?"}
    YN = {"owner": {"q": {"tck.ow.a": "Is {s} the owner of ticket {e} {when}?",
                          "tck.ow.b": "Under the numbered rules, does ticket {e} belong to {s} {when}?"},
                    "neg": {"tck.own.a": "Is ticket {e} owned by someone other than {s} {when}, or by nobody?"},
                    "card": {"yes": "Under the rules the named person is the ticket's owner at the stated time.",
                             "no": "At the stated time the ticket has another owner or no owner."},
                    "ncard": {"yes": "At the stated time the ticket has another owner or no owner.",
                              "no": "Under the rules the named person is the ticket's owner at the stated time."},
                    "jb": ("{s} owns ticket {e} {when}.", "{s} does not own ticket {e} {when}.")},
          "overdue": {"q": {"tck.od.a": "Is ticket {e} overdue {when} under the SLA rules?",
                            "tck.od.b": "Had ticket {e} missed its resolution due time {when}?"},
                      "neg": {"tck.odn.a": "Is ticket {e} still within its SLA {when}, with no missed due time?"},
                      "card": {"yes": "The stated time is after the ticket's due time and the ticket had not first "
                                      "reached resolved by the due time.",
                               "no": "The due time has not passed at the stated time, or the ticket first reached "
                                     "resolved at or before its due time."},
                      "ncard": {"yes": "The due time has not passed at the stated time, or the ticket first "
                                       "reached resolved at or before its due time.",
                                "no": "The stated time is after the due time and the ticket had not first reached "
                                      "resolved by then."},
                      "jb": ("Ticket {e} is overdue {when}.", "Ticket {e} is not overdue {when}.")}}

    def queries(self, W, qtype, rng):
        if qtype in ("value", "judge"):
            return [Query(qtype, "owner", ("owner", W.target))]
        if qtype == "yn":
            return [Query("yn", "owner", ("owner", W.target)), Query("yn", "overdue", ("overdue", W.target))]
        return [Query("score", "level", ("level", W.target))]

    def pred(self, W, q, v):
        return v == q.arg if q.fam == "owner" else bool(v)

    def levels(self, W, q):
        return list(self.LEVELS)

    def level(self, W, q, obs):
        return obs[("level", W.target)]

    def qfields(self, W, q):
        return {"e": W.target, "s": q.arg}

    def text_fields(self, e, W):
        return {}


# ================================================================================================ F3.3 access
class Access(Machine):
    """Resource access: roles viewer < editor < owner, grants (optionally timed), revokes, deny-overrides, group
    membership and group renames; only listed admins may change access."""
    name, noun, plural, ent_prefix = "access", "resource", "resources", "RES-"
    gap = (3, 150)
    has_expiry = True
    has_revert = False
    ROLES = ("viewer", "editor", "owner")
    RANK = {"viewer": 1, "editor": 2, "owner": 3}
    VALS = ("no access", "viewer", "editor", "owner", "blocked by a deny")
    SRC = {}
    TXT = {"grant": ("grant role={role} to={to} resource={e}{hrs_s}", ("{by} gave {to} the {role} role on {e}{hrs_l}.",
                                                                       "{to} was granted {role} access to {e}{hrs_l}.")),
           "revoke": ("revoke grant={of}", ("{by} revoked the grant made in event {of}.",
                                            "Grant {of} withdrawn by {by}.")),
           "deny": ("deny user={to} resource={e}", ("{by} blocked {to} from {e}.", "Deny rule added: {to} on {e}.")),
           "undeny": ("lift_deny user={to} resource={e}", ("{by} lifted the block on {to} for {e}.",
                                                           "Deny rule for {to} on {e} removed.")),
           "join": ("add_member user={to} group={g}", ("{by} added {to} to group {g}.", "{to} joined group {g}.")),
           "leave": ("remove_member user={to} group={g}", ("{by} removed {to} from group {g}.",
                                                          "{to} left group {g}.")),
           "rename": ("rename_group from={g} to={g2}", ("{by} renamed group {g} to {g2}.",
                                                        "Group {g} is now called {g2}."))}

    def text_fields(self, e, W):
        h = e.a.get("hours")
        return {"by": e.src, "hrs_s": f" hours={h}" if h else "", "hrs_l": f" for {h} hours" if h else ""}

    def new_world(self, rng, pool, spec):
        used = set()
        ids = self.ent_ids(rng, 1, used)
        ents = {ids[0]: {"kind": rng.choice(["shared folder", "repository", "dashboard", "ledger export"])}}
        W = base_world(self, rng, pool, spec, ents, ids[0])
        nu = spec.n_ent or rng.randint(3, 5)
        users = []
        while len(users) < nu:
            p = pool.person(rng)
            if p not in users:
                users.append(p)
        admins = []
        while len(admins) < 2:
            p = pool.person(rng)
            if p not in users and p not in admins:
                admins.append(p)
        outsider = pool.person(rng)
        while outsider in users or outsider in admins:
            outsider = pool.person(rng)
        groups = sorted({f"{pool.stem(rng).lower()}-team" for _ in range(2)})
        members = {g: sorted(rng.sample(users, rng.randint(0, 2))) for g in groups}
        W.params = {"users": users, "admins": admins, "outsider": outsider, "groups": groups, "members": members,
                    "user": users[0], "renamed": {}}
        self._srcs(W)
        self.mix_offsets(W, rng, spec)
        if spec.traps.get("decoy"):
            self.add_decoy(rng, W, used, rng.random() < 0.5, dict(ents[ids[0]]))
        return W

    def _srcs(self, W):
        W.offsets = {p: W.offsets.get(p, 0) for p in W.params["admins"] + [W.params["outsider"]]}

    def other_ent(self, W, rng):
        return W.target

    def init(self, W):
        return {"_": {"grants": {}, "deny": {}, "members": {g: list(m) for g, m in W.params["members"].items()},
                      "names": {g: g for g in W.params["groups"]}},
                **{k: {} for k in W.ents}}

    def _gkey(self, st, name):
        for k, v in st["_"]["names"].items():
            if v == name:
                return k
        return None

    def apply(self, st, e, ent, W, flags):
        G = st["_"]
        guards = "guards" not in flags
        if guards and e.src not in W.params["admins"]:
            return "guard"
        k = e.kind
        if k in ("grant", "deny", "undeny") and ent not in st:
            return "unknown"
        if k == "grant":
            to = e.a["to"]
            if to.endswith("-team"):
                gk = self._gkey(st, to)
                if gk is None:
                    return "unknown" if guards else "unknown"
                to = ("group", gk)
            else:
                to = ("user", to)
            exp = e.ts + timedelta(hours=e.a["hours"]) if e.a.get("hours") else None
            gid = e.eid if e.eid not in G["grants"] else e.eid + "#" + str(e.idx)
            G["grants"][gid] = {"to": to, "res": ent, "role": e.a["role"], "exp": exp, "revoked": False,
                                "eid": e.eid}
            return [("pop", "_", "grants", gid)]
        if k == "revoke":
            g = G["grants"].get(e.a["of"])
            if g is None or g["revoked"]:
                return "guard"
            g["revoked"] = True
            return []
        if k in ("deny", "undeny"):
            key = (e.a["to"], ent)
            old = G["deny"].get(key, False)
            G["deny"][key] = (k == "deny")
            return []
        if k in ("join", "leave"):
            gk = self._gkey(st, e.a["g"])
            if gk is None:
                return "unknown"
            m = G["members"][gk]
            if k == "join" and e.a["to"] not in m:
                m.append(e.a["to"])
            elif k == "leave":
                if e.a["to"] not in m:
                    return "guard"
                m.remove(e.a["to"])
            return []
        if k == "rename":
            gk = self._gkey(st, e.a["g"])
            if gk is None or self._gkey(st, e.a["g2"]) is not None:
                return "unknown"
            G["names"][gk] = e.a["g2"]
            return []
        raise ValueError(k)

    def role(self, st, W, user, res, flags):
        G = st["_"]
        if G["deny"].get((user, res)):
            return "blocked by a deny"
        best = 0
        for g in G["grants"].values():
            if g["res"] != res or g["revoked"]:
                continue
            if g["exp"] is not None and g["exp"] <= W.t_q and "expiry" not in flags:
                continue
            ok = g["to"] == ("user", user) or (g["to"][0] == "group" and user in G["members"].get(g["to"][1], []))
            if ok:
                best = max(best, self.RANK[g["role"]])
        return ("no access", "viewer", "editor", "owner")[best]

    def observe(self, st, W, flags):
        return {("access", u): self.role(st, W, u, W.target, flags) for u in W.params["users"]}

    def moves(self, st, W, ent, t, rng, mode):
        P = W.params
        adm = P["admins"]
        u0 = P["user"]
        G = st["_"]
        names = sorted(G["names"].values())
        res = ent if ent is not None else W.target
        if mode == "guard":
            return [("grant", {"role": rng.choice(["editor", "owner"]), "to": u0, "hours": None}, P["outsider"]),
                    ("revoke", {"of": pick(rng, sorted(G["grants"])) or "E0000"}, P["outsider"]),
                    ("grant", {"role": "editor", "to": pick(rng, names), "hours": None}, P["outsider"])]
        who = rng.choice(adm)
        tgt_user = u0 if mode in ("main", "expiry", "after", "decoy") else rng.choice(P["users"])
        out = [("grant", {"role": rng.choice(self.ROLES), "to": tgt_user,
                          "hours": rng.choice([None, None, 2, 4, 8]) if mode != "expiry" else rng.choice([1, 2, 3])},
                who)]
        if mode == "expiry":
            return out
        live = [g for g, v in G["grants"].items() if not v["revoked"] and "#" not in g]
        if live and mode in ("main", "other"):
            out.append(("revoke", {"of": rng.choice(sorted(live))}, who))
        if mode in ("main", "other"):
            if not G["deny"].get((tgt_user, res)):
                if rng.random() < 0.35:
                    out.append(("deny", {"to": tgt_user}, who))
            else:
                out.append(("undeny", {"to": tgt_user}, who))
            g = pick(rng, names)
            gk = self._gkey(st, g)
            if gk is not None:
                if tgt_user in G["members"][gk]:
                    out.append(("leave", {"to": tgt_user, "g": g}, who))
                else:
                    out.append(("join", {"to": tgt_user, "g": g}, who))
                out.append(("grant", {"role": rng.choice(self.ROLES), "to": g, "hours": None}, who))
                if rng.random() < 0.15:
                    out.append(("rename", {"g": g, "g2": f"{g[:-5]}{rng.choice(['ops', 'core', 'field'])}-team"},
                                who))
        for k, a, s in out:
            if k in ("join", "leave", "rename", "revoke"):
                a["_ent"] = None
            else:
                a["_ent"] = res
        return out

    def expiring(self, W):
        return any(e.kind == "grant" and e.a.get("hours") and e.ts <= W.t_q for e in W.events)

    def rules(self, W):
        P = W.params
        return (["Roles on a resource rank viewer < editor < owner. A person's access is the highest role among the "
                 "grants in force for them, given to them directly or to a group they belong to at the stated time.",
                 f"Only these admins may change access: {', '.join(P['admins'])}. A change logged by anyone else is "
                 "rejected and changes nothing.",
                 "A grant with a number of hours stops counting at its start time plus those hours (it no longer "
                 "counts at exactly that time). A grant without hours lasts until it is revoked.",
                 "A revoke names the event id of an earlier grant; that grant stops counting. A revoke of a grant "
                 "that never took effect, or is already revoked, changes nothing.",
                 "A deny rule blocks the person from the resource whatever grants they hold, until the deny rule is "
                 "lifted.",
                 "Renaming a group keeps its members and grants. After a rename, only the new name refers to the "
                 "group; a line using the old name changes nothing.",
                 "Viewing needs viewer or higher; editing needs editor or higher."]
                + self.common_rules(W, revert=False))

    def start_rows(self, W):
        P = W.params
        rows = [(k, [("kind", v["kind"]), ("grants", "none")]) for k, v in W.ents.items()]
        rows += [(g, [("members", ", ".join(P["members"][g]) or "none")]) for g in P["groups"]]
        return rows

    def context(self, W):
        return [("system", "access registry"), ("people tracked", ", ".join(W.params["users"]))]

    def label(self, key, W):
        return f"{key[1]} access on {W.target}"

    def vtext(self, key, v, W):
        return v

    def last_event(self, W, key):
        u = key[1]
        v = None
        grants = {e.eid: e for e in W.events if e.kind == "grant"}
        for e in time_order(W):
            if e.ts > W.t_q:
                continue
            if e.kind == "grant" and e.a["to"] == u and e.ent == W.target:
                v = e.a["role"]
            elif e.kind == "deny" and e.a["to"] == u and e.ent == W.target:
                v = "blocked by a deny"
            elif e.kind == "revoke" and e.a["of"] in grants and grants[e.a["of"]].a["to"] == u:
                v = "no access"
        return v

    def domain(self, W, q):
        return list(self.VALS)

    DEFS = {"no access": "no grant in force gives this person any role and no deny applies",
            "viewer": "the highest role in force is viewer", "editor": "the highest role in force is editor",
            "owner": "the highest role in force is owner",
            "blocked by a deny": "a deny rule in force blocks this person whatever grants they hold"}

    def option_defs(self, q, opts):
        return {o: self.DEFS[o] for o in sorted(opts) if o in self.DEFS}

    VALUE_TPL = {"acc.v.a": "What access does {u} have to {e} {when}, under the numbered rules?",
                 "acc.v.b": "Under the access rules, which access level applies to {u} on {e} {when}?"}
    SCORE_TPL = {"acc.sc.a": "How many of the tracked people can edit {e} {when}?",
                 "acc.sc.b": "Under the access rules, how many tracked people hold editing access to {e} {when}?"}
    YN = {"edit": {"q": {"acc.ed.a": "Can {u} edit {e} {when}?",
                         "acc.ed.b": "Under the numbered rules, is {u} allowed to edit {e} {when}?"},
                   "neg": {"acc.edn.a": "Is {u} unable to edit {e} {when}?"},
                   "card": {"yes": "At the stated time the person holds editor or owner through a grant in force, "
                                   "and no deny rule blocks them.",
                            "no": "At the stated time the person holds no editor or owner grant in force, or a deny "
                                  "rule blocks them."},
                   "ncard": {"yes": "At the stated time the person holds no editor or owner grant in force, or a "
                                    "deny rule blocks them.",
                             "no": "At the stated time the person holds editor or owner through a grant in force and "
                                   "no deny rule blocks them."},
                   "jb": ("{u} can edit {e} {when}.", "{u} cannot edit {e} {when}.")},
          "view": {"q": {"acc.vw.a": "Can {u} open {e} for viewing {when}?",
                         "acc.vw.b": "Under the numbered rules, does {u} have at least viewer access to {e} {when}?"},
                   "neg": {"acc.vwn.a": "Is {u} shut out of viewing {e} {when}?"},
                   "card": {"yes": "At the stated time the person holds viewer or higher through a grant in force, "
                                   "and no deny rule blocks them.",
                            "no": "At the stated time the person holds no grant in force, or a deny rule blocks them."},
                   "ncard": {"yes": "At the stated time the person holds no grant in force, or a deny rule blocks "
                                    "them.",
                             "no": "At the stated time the person holds viewer or higher through a grant in force and "
                                   "no deny rule blocks them."},
                   "jb": ("{u} can view {e} {when}.", "{u} cannot view {e} {when}.")}}

    def queries(self, W, qtype, rng):
        k = ("access", W.params["user"])
        if qtype in ("value", "judge"):
            return [Query(qtype, "access", k)]
        if qtype == "yn":
            return [Query("yn", "edit", k), Query("yn", "view", k)]
        return [Query("score", "editors", None, None, tuple(("access", u) for u in W.params["users"]))]

    def pred(self, W, q, v):
        r = {"no access": 0, "viewer": 1, "editor": 2, "owner": 3, "blocked by a deny": -1}[v]
        return r >= (2 if q.fam == "edit" else 1)

    def levels(self, W, q):
        n = len(q.keys)
        return [f"{i} of the {n} tracked people" if i else f"none of the {n} tracked people" for i in range(n + 1)]

    def level(self, W, q, obs):
        return sum(1 for k in q.keys if obs.get(k) in ("editor", "owner"))

    def qfields(self, W, q):
        return {"e": W.target, "u": W.params["user"]}


# ================================================================================================ F3.4 inventory
class Inventory(Machine):
    name, noun, plural, ent_prefix, ent_digits = "inventory", "SKU", "SKUs", "SKU-", 6
    gap = (3, 90)
    has_expiry = True
    SRC = {"receive": "receiving", "ship": "picking", "hold": "sales-orders", "release": "sales-orders",
           "quarantine": "quality", "clear": "quality", "count": "cycle-count", "revert": "ops-console"}
    TXT = {"receive": ("receive sku={e} qty={q}", ("Received {q} {units} of {e} at the dock.",
                                                  "Inbound pallet: {q} {units} of {e} put away.")),
           "ship": ("ship sku={e} qty={q}", ("Picked and shipped {q} {units} of {e}.", "{q} {units} of {e} left on an "
                                                                                   "outbound order.")),
           "hold": ("hold sku={e} qty={q} minutes={m}", ("Reserved {q} {units} of {e} for {m} minutes.",
                                                        "Hold placed: {q} {units} of {e}, valid {m} minutes.")),
           "release": ("release hold={of}", ("Hold {of} released.", "Customer dropped the reservation made in "
                                                                    "event {of}.")),
           "quarantine": ("quarantine sku={e} qty={q}", ("{q} {units} of {e} moved to quarantine.",
                                                         "Quality flagged {q} {units} of {e} for quarantine.")),
           "clear": ("clear_quarantine sku={e} qty={q}", ("{q} quarantined {units} of {e} cleared for sale.",
                                                          "Quality released {q} {units} of {e} from quarantine.")),
           "count": ("count sku={e} on_hand={q}", ("Cycle count: {e} has {q} {units} on hand.",
                                                   "Shelf count for {e} came to {q} {units}.")),
           "revert": ("revert event={of}", ("Reversal of event {of} posted.", "Operator reverted event {of}."))}
    BUCKETS = ((0, 0), (1, 4), (5, 9), (10, 19), (20, 10 ** 9))

    def text_fields(self, e, W):
        return {"units": "unit" if e.a.get("q") == 1 else "units"}
    revert_rule = ("A revert line names an earlier event id. If that event took effect and has not been reverted yet, "
                   "its own change is undone: units it received are taken off again (never below 0), units it shipped "
                   "are put back, "
                   "a hold it placed is removed, a hold it released comes back, units it quarantined return to "
                   "available (never below 0 in quarantine), units it cleared go back into quarantine, and a cycle "
                   "count's on-hand number goes back "
                   "to what it was just before the count. Later events keep their effect. Otherwise the revert "
                   "changes nothing.")
    LEVELS = ("0 units", "1 to 4 units", "5 to 9 units", "10 to 19 units", "20 units or more")

    def new_world(self, rng, pool, spec):
        used = set()
        n = spec.n_ent or rng.randint(1, 3)
        ids = self.ent_ids(rng, n, used)
        ents = {x: {"on_hand": rng.randint(0, 14), "item": rng.choice(["bracket", "hinge", "cable", "lamp", "valve",
                                                                       "filter", "gasket", "sensor"])}
                for x in ids}
        W = base_world(self, rng, pool, spec, ents, ids[0])
        W.params = {"site": pool.stem(rng) + " warehouse"}
        if spec.traps.get("decoy"):
            self.add_decoy(rng, W, used, rng.random() < 0.6, {"on_hand": rng.randint(0, 14),
                                                              "item": ents[ids[0]]["item"]})
        return W

    def init(self, W):
        return {k: {"on": v["on_hand"], "holds": {}, "quar": 0} for k, v in W.ents.items()}

    def avail(self, s, t, flags):
        h = sum(q for q, exp in s["holds"].values() if "expiry" in flags or exp > t)
        return max(0, s["on"] - h - s["quar"])

    def apply(self, st, e, ent, W, flags):
        if e.kind == "release":
            for k, s in st.items():
                if e.a["of"] in s["holds"]:
                    q, exp = s["holds"][e.a["of"]]
                    if exp <= e.ts and "expiry" not in flags and "guards" not in flags:
                        return "guard"
                    s["holds"].pop(e.a["of"])
                    return [("put", k, "holds", e.a["of"], (q, exp))]
            return "guard"
        if ent not in st:
            return "unknown"
        s = st[ent]
        g = "guards" not in flags
        q = e.a.get("q", 0)
        k = e.kind
        if k == "receive":
            s["on"] += q
            return [("sub0", ent, "on", q)]
        if k in ("ship", "hold", "quarantine"):
            if g and q > self.avail(s, e.ts, flags):
                return "guard"
            if k == "ship":
                s["on"] -= q
                return [("add", ent, "on", -q)]
            if k == "hold":
                hid = e.eid if e.eid not in s["holds"] else f"{e.eid}#{e.idx}"
                s["holds"][hid] = (q, e.ts + timedelta(minutes=e.a["m"]))
                return [("pop", ent, "holds", hid)]
            s["quar"] += q
            return [("sub0", ent, "quar", q)]
        if k == "clear":
            if g and q > s["quar"]:
                return "guard"
            s["quar"] -= q
            return [("add", ent, "quar", -q)]
        if k == "count":
            old = s["on"]
            s["on"] = q
            return [("set", ent, "on", old)]
        raise ValueError(k)

    def moves(self, st, W, ent, t, rng, mode):
        if ent not in st:
            return [("receive", {"q": rng.randint(2, 12)}, self.SRC["receive"]),
                    ("count", {"q": rng.randint(0, 20)}, self.SRC["count"])]
        s = st[ent]
        av = self.avail(s, t, frozenset())
        if mode == "guard":
            out = [(k, {"q": av + rng.randint(1, 6)}, self.SRC[k]) for k in ("ship", "quarantine")]
            out.append(("hold", {"q": av + rng.randint(1, 4), "m": rng.choice([30, 60, 120])}, self.SRC["hold"]))
            if s["quar"] < 6:
                out.append(("clear", {"q": s["quar"] + rng.randint(1, 4)}, self.SRC["clear"]))
            return out
        if mode == "expiry":
            return [("hold", {"q": rng.randint(1, max(1, av)), "m": rng.choice([10, 15, 20, 30])}, self.SRC["hold"])] \
                if av >= 1 else [("receive", {"q": rng.randint(2, 9)}, self.SRC["receive"])]
        out = [("receive", {"q": rng.randint(1, 12)}, self.SRC["receive"])]
        if av >= 1:
            out += [("ship", {"q": rng.randint(1, av)}, self.SRC["ship"]),
                    ("hold", {"q": rng.randint(1, av), "m": rng.choice([15, 30, 60, 240, 720])}, self.SRC["hold"]),
                    ("quarantine", {"q": rng.randint(1, min(av, 5))}, self.SRC["quarantine"])]
        if s["quar"] > 0:
            out.append(("clear", {"q": rng.randint(1, s["quar"])}, self.SRC["clear"]))
        live = [h for h, (q, exp) in s["holds"].items() if exp > t and "#" not in h]
        if live:
            out.append(("release", {"of": rng.choice(sorted(live)), "_ent": ent}, self.SRC["release"]))
        if rng.random() < 0.3:
            out.append(("count", {"q": max(0, s["on"] + rng.randint(-3, 3))}, self.SRC["count"]))
        return out

    def expiring(self, W):
        return any(e.kind == "hold" and e.ts <= W.t_q for e in W.events)

    def observe(self, st, W, flags):
        out = {}
        for k in W.ents:
            out[("avail", k)] = self.avail(st[k], W.t_q, flags)
        return out

    def rules(self, W):
        return (["Available units = units on hand minus units under an active hold minus units in quarantine "
                 "(never below 0).",
                 "A receive adds units on hand. A ship removes units on hand and is allowed only if that many units "
                 "are available at that moment. A hold reserves units for the stated number of minutes and is "
                 "allowed only if that many units are available; it stops counting at its start time plus those "
                 "minutes (it no longer counts at exactly that time), or when it is released.",
                 "A release names the event id of an earlier hold that is still active; otherwise it changes "
                 "nothing. A quarantine moves available units into quarantine (only if that many are available); a "
                 "clear returns quarantined units (only up to the number in quarantine).",
                 "A cycle count sets the units on hand to the counted number; holds and quarantine stay as they are.",
                 "Language lines map to the same steps: received or put away is receive, picked and shipped or left "
                 "on an outbound order is ship, reserved or hold placed is hold, released or dropped reservation is "
                 "release, moved to or flagged into quarantine is quarantine, cleared or released from quarantine is "
                 "clear, a cycle or shelf count is count, and a reversal or revert line is a revert."]
                + self.common_rules(W))

    def start_rows(self, W):
        return [(k, [("item", v["item"]), ("on hand", str(v["on_hand"])), ("holds", "none"), ("quarantine", "0")])
                for k, v in W.ents.items()]

    def context(self, W):
        return [("system", "warehouse stock ledger"), ("site", W.params["site"])]

    def label(self, key, W):
        return f"{key[1]} available units"

    def vtext(self, key, v, W):
        return f"{v} units" if v != 1 else "1 unit"

    def domain(self, W, q):
        return None

    def option_defs(self, q, opts):
        return None

    VALUE_TPL = {"inv.v.a": "How many units of {e} are available {when}, under the numbered rules?",
                 "inv.v.b": "Under the stock rules, what is the available quantity of {e} {when}?"}
    SCORE_TPL = {"inv.sc.a": "Which band does the available quantity of {e} fall in {when}?",
                 "inv.sc.b": "Under the stock rules, in which availability band is {e} {when}?"}
    YN = {"ge": {"q": {"inv.ge.a": "Are at least {s} units of {e} available {when}?",
                       "inv.ge.b": "Under the numbered rules, does {e} have {s} or more units available {when}?"},
                 "neg": {"inv.gen.a": "Are fewer than {s} units of {e} available {when}?"},
                 "card": {"yes": "Under the rules the available units (on hand minus active holds minus quarantine) "
                                 "at the stated time are at least the named number.",
                          "no": "The available units at the stated time are below the named number."},
                 "ncard": {"yes": "The available units at the stated time are below the named number.",
                           "no": "Under the rules the available units at the stated time are at least the named "
                                 "number."},
                 "jb": ("At least {s} units of {e} are available {when}.",
                        "Fewer than {s} units of {e} are available {when}.")}}

    def queries(self, W, qtype, rng):
        k = ("avail", W.target)
        if qtype in ("value", "judge"):
            return [Query(qtype, "avail", k)]
        if qtype == "yn":
            return [Query("yn", "ge", k)]
        return [Query("score", "band", k)]

    def pred(self, W, q, v):
        return v >= q.arg

    def levels(self, W, q):
        return list(self.LEVELS)

    def level(self, W, q, obs):
        v = obs[q.key]
        return next(i for i, (lo, hi) in enumerate(self.BUCKETS) if lo <= v <= hi)

    def qfields(self, W, q):
        return {"e": W.target, "s": q.arg}


# ================================================================================================ F3.5 bookings
class Bookings(Machine):
    name, noun, plural, ent_prefix, ent_digits = "bookings", "slot", "slots", "DESK-", 4
    gap = (1, 14)
    has_expiry = True
    TXT = {"hold": ("hold slot={e} user={u} minutes={m}", ("{u} put a {m}-minute hold on {e}.",
                                                          "Hold on {e} for {u}, valid {m} minutes.")),
           "confirm": ("confirm slot={e} user={u}", ("{u} confirmed the booking of {e}.",
                                                     "Booking of {e} confirmed by {u}.")),
           "cancel": ("cancel slot={e} user={u}", ("{u} cancelled the booking of {e}.",
                                                   "Booking of {e} cancelled by {u}.")),
           "release": ("release slot={e} user={u}", ("{u} let the hold on {e} go.", "{u} released the hold on {e}.")),
           "revert": ("revert event={of}", ("Front desk reverted event {of}.", "Undo of event {of} requested."))}
    SRC = {"hold": "booking-app", "confirm": "booking-app", "cancel": "booking-app", "release": "booking-app",
           "revert": "front-desk"}

    def new_world(self, rng, pool, spec):
        used = set()
        n = spec.n_ent or rng.randint(2, 4)
        ids = self.ent_ids(rng, n, used)
        users = []
        while len(users) < 3:
            p = pool.person(rng)
            if p not in users:
                users.append(p)
        ents = {x: {"booked": None if i == 0 or rng.random() < 0.6 else rng.choice(users)} for i, x in enumerate(ids)}
        W = base_world(self, rng, pool, spec, ents, ids[0])
        W.params = {"users": users, "user": users[0], "hold_default": rng.choice([10, 15, 20])}
        if spec.traps.get("decoy"):
            self.add_decoy(rng, W, used, rng.random() < 0.6, {"booked": None})
        return W

    def init(self, W):
        return {k: {"booked": v["booked"], "hold": None} for k, v in W.ents.items()}

    def _active(self, s, t, flags):
        h = s["hold"]
        return h if (h is not None and ("expiry" in flags or h[1] > t)) else None

    def apply(self, st, e, ent, W, flags):
        if ent not in st:
            return "unknown"
        s = st[ent]
        g = "guards" not in flags
        u = e.a["u"]
        h = self._active(s, e.ts, flags)
        k = e.kind
        if k == "hold":
            if g and (s["booked"] is not None or (h is not None and h[0] != u)):
                return "guard"
            old = s["hold"]
            s["hold"] = (u, e.ts + timedelta(minutes=e.a["m"]))
            return [("set", ent, "hold", old)]
        if k == "confirm":
            if g and (h is None or h[0] != u):
                return "guard"
            old = (s["booked"], s["hold"])
            s["booked"], s["hold"] = u, None
            return [("set", ent, "booked", old[0]), ("set", ent, "hold", old[1])]
        if k == "cancel":
            if g and s["booked"] != u:
                return "guard"
            old = s["booked"]
            s["booked"] = None
            return [("set", ent, "booked", old)]
        if k == "release":
            if g and (h is None or h[0] != u):
                return "guard"
            old = s["hold"]
            s["hold"] = None
            return [("set", ent, "hold", old)]
        raise ValueError(k)

    def moves(self, st, W, ent, t, rng, mode):
        U = W.params["users"]
        if ent not in st:
            return [("hold", {"u": rng.choice(U), "m": W.params["hold_default"]}, self.SRC["hold"]),
                    ("confirm", {"u": rng.choice(U)}, self.SRC["confirm"])]
        s = st[ent]
        h = self._active(s, t, frozenset())
        m = W.params["hold_default"]
        if mode == "guard":
            out = []
            others = [x for x in U if x != (h[0] if h else s["booked"])]
            out.append(("confirm", {"u": rng.choice(others or U)}, self.SRC["confirm"]))
            if s["booked"] is not None:
                out.append(("hold", {"u": rng.choice(U), "m": m}, self.SRC["hold"]))
                out.append(("cancel", {"u": rng.choice([x for x in U if x != s["booked"]] or U)}, self.SRC["cancel"]))
            return out
        pref = W.params["user"] if mode in ("main", "expiry", "after") and rng.random() < 0.7 else rng.choice(U)
        out = []
        if s["booked"] is None and (h is None or h[0] == pref):
            out.append(("hold", {"u": pref, "m": m if mode != "expiry" else rng.choice([5, 10])}, self.SRC["hold"]))
        if mode == "expiry":
            return out
        if h is not None:
            out.append(("confirm", {"u": h[0]}, self.SRC["confirm"]))
            if rng.random() < 0.3:
                out.append(("release", {"u": h[0]}, self.SRC["release"]))
        if s["booked"] is not None:
            out.append(("cancel", {"u": s["booked"]}, self.SRC["cancel"]))
        return out

    def expiring(self, W):
        return any(e.kind == "hold" and e.ts <= W.t_q for e in W.events)

    def observe(self, st, W, flags):
        out = {}
        for k in W.ents:
            s = st[k]
            out[("booked", k)] = s["booked"] or "nobody"
            out[("free", k)] = s["booked"] is None and self._active(s, W.t_q, flags) is None
        return out

    def rules(self, W):
        return ([f"A hold reserves a slot for one person for the stated minutes (default {W.params['hold_default']}). "
                 "It stops counting at its start time plus those minutes (it no longer counts at exactly that time).",
                 "A hold is allowed only if the slot has no confirmed booking and no active hold by another person.",
                 "A confirmation is allowed only for the person whose hold on that slot is active at that moment; it "
                 "turns the hold into that person's confirmed booking.",
                 "A cancellation is allowed only for the person who holds the confirmed booking; it frees the slot. "
                 "A release is allowed only for the person whose hold is active; it ends the hold.",
                 "A slot is free for a new hold when it has no confirmed booking and no active hold.",
                 "Language lines map to the same steps: put a hold or hold on is hold, confirmed is confirm, "
                 "cancelled is cancel, let the hold go or released the hold is release, and an undo or revert line "
                 "is a revert."]
                + self.common_rules(W))

    def start_rows(self, W):
        return [(k, [("confirmed booking", v["booked"] or "none"), ("hold", "none")]) for k, v in W.ents.items()]

    def context(self, W):
        return [("system", "desk booking"), ("people", ", ".join(W.params["users"]))]

    def label(self, key, W):
        return f"{key[1]} confirmed booking" if key[0] == "booked" else f"{key[1]} free"

    def vtext(self, key, v, W):
        return v if key[0] == "booked" else ("yes" if v else "no")

    def last_event(self, W, key):
        if key[0] != "booked":
            return None
        v = None
        for e in time_order(W):
            if e.ts <= W.t_q and e.ent == key[1]:
                if e.kind == "confirm":
                    v = e.a["u"]
                elif e.kind == "cancel":
                    v = "nobody"
        return v

    def domain(self, W, q):
        return list(W.params["users"]) + ["nobody"]

    def option_defs(self, q, opts):
        return None

    VALUE_TPL = {"bkg.v.a": "Who holds the confirmed booking of {e} {when}, under the numbered rules?",
                 "bkg.v.b": "Under the booking rules, whose confirmed booking is {e} {when}?"}
    SCORE_TPL = {"bkg.sc.a": "How many of the listed slots have a confirmed booking {when}?",
                 "bkg.sc.b": "Under the booking rules, how many listed slots are booked and confirmed {when}?"}
    YN = {"booked": {"q": {"bkg.bk.a": "Does {u} hold the confirmed booking of {e} {when}?",
                           "bkg.bk.b": "Under the numbered rules, is {e} booked and confirmed for {u} {when}?"},
                     "neg": {"bkg.bkn.a": "Is {e} without a confirmed booking for {u} {when}?"},
                     "card": {"yes": "Under the rules the named person holds the confirmed booking of the slot at the "
                                     "stated time.",
                              "no": "At the stated time the slot has no confirmed booking or another person's."},
                     "ncard": {"yes": "At the stated time the slot has no confirmed booking or another person's.",
                               "no": "Under the rules the named person holds the confirmed booking at the stated "
                                     "time."},
                     "jb": ("{u} holds the confirmed booking of {e} {when}.",
                            "{u} does not hold the confirmed booking of {e} {when}.")},
          "free": {"q": {"bkg.fr.a": "Is {e} free for a new hold {when}?",
                         "bkg.fr.b": "Under the numbered rules, could anyone place a new hold on {e} {when}?"},
                   "neg": {"bkg.frn.a": "Is {e} taken {when}, by a confirmed booking or an active hold?"},
                   "card": {"yes": "At the stated time the slot has no confirmed booking and no active hold.",
                            "no": "At the stated time the slot has a confirmed booking or an active hold."},
                   "ncard": {"yes": "At the stated time the slot has a confirmed booking or an active hold.",
                             "no": "At the stated time the slot has no confirmed booking and no active hold."},
                   "jb": ("{e} is free for a new hold {when}.", "{e} is not free for a new hold {when}.")}}

    def queries(self, W, qtype, rng):
        if qtype in ("value", "judge"):
            return [Query(qtype, "booked", ("booked", W.target))]
        if qtype == "yn":
            return [Query("yn", "booked", ("booked", W.target)), Query("yn", "free", ("free", W.target))]
        return [Query("score", "count", None, None, tuple(("booked", x) for x in W.ents))]

    def pred(self, W, q, v):
        return v == W.params["user"] if q.fam == "booked" else bool(v)

    def levels(self, W, q):
        n = len(q.keys)
        return [f"{i} of the {n} listed slots" if i else f"none of the {n} listed slots" for i in range(n + 1)]

    def level(self, W, q, obs):
        return sum(1 for k in q.keys if obs.get(k) not in (None, "nobody"))

    def qfields(self, W, q):
        return {"e": W.target, "u": W.params["user"]}


# ================================================================================================ F3.6 ledger
class Ledger(Machine):
    name, noun, plural, ent_prefix, ent_digits = "ledger", "account", "accounts", "ACC-", 7
    gap = (20, 300)
    has_expiry = True
    SRC = {"deposit": "core-banking", "auth": "card-network", "post": "card-network", "fee": "billing",
           "transfer": "payments-hub", "revert": "back-office"}
    TXT = {"deposit": ("deposit account={e} amount={amt}", ("{amt} credited to account {e}.",
                                                           "Incoming payment of {amt} to {e} settled.")),
           "auth": ("authorise account={e} amount={amt}", ("Card authorisation of {amt} on {e}.",
                                                          "Merchant hold of {amt} placed on account {e}.")),
           "post": ("post auth={of}", ("Authorisation {of} posted.", "Merchant settled the hold from event {of}.")),
           "fee": ("fee account={e} amount={amt}", ("Monthly fee of {amt} charged to {e}.",
                                                    "Service charge of {amt} booked on {e}.")),
           "transfer": ("transfer_out account={e} amount={amt}", ("Transfer of {amt} sent from {e}.",
                                                                  "{e} paid out {amt} by transfer.")),
           "revert": ("reverse event={of}", ("Event {of} reversed by the bank.", "Reversal of event {of} booked."))}
    LEVELS = ("below 100.00", "100.00 to 499.99", "500.00 to 1,999.99", "2,000.00 or more")
    revert_rule = ("A reversal line names an earlier event id. If that event took effect and has not been reversed "
                   "yet, its own change is undone: a deposit's amount is taken off again, a fee's or transfer's amount "
                   "is added back, an authorisation stops being pending, and a post adds its amount back and makes "
                   "the authorisation pending again with its original lapse time. Later events keep their effect. "
                   "Otherwise the reversal changes nothing.")
    BOUNDS = (10000, 50000, 200000)

    def text_fields(self, e, W):
        return {"amt": money(e.a["c"], W.params["cur"])} if "c" in e.a else {}

    def new_world(self, rng, pool, spec):
        used = set()
        n = spec.n_ent or rng.randint(1, 2)
        ids = self.ent_ids(rng, n, used)
        ents = {x: {"posted": rng.randint(0, 3000) * 100 + rng.choice([0, 50, 99]), "holder": pool.person(rng)}
                for x in ids}
        W = base_world(self, rng, pool, spec, ents, ids[0])
        W.params = {"cur": rng.choice(["EUR", "USD", "GBP", "CHF"]), "lapse": rng.choice([6, 12, 24])}
        if spec.traps.get("decoy"):
            self.add_decoy(rng, W, used, rng.random() < 0.6, {"posted": rng.randint(0, 3000) * 100,
                                                              "holder": ents[ids[0]]["holder"]})
        return W

    def init(self, W):
        return {k: {"posted": v["posted"], "pend": {}, "tx": {}} for k, v in W.ents.items()}

    def avail(self, s, t, flags):
        return s["posted"] - sum(c for c, exp in s["pend"].values() if "expiry" in flags or exp > t)

    def apply(self, st, e, ent, W, flags):
        g = "guards" not in flags
        if e.kind == "post":
            for k, s in st.items():
                if e.a["of"] in s["pend"]:
                    c, exp = s["pend"][e.a["of"]]
                    if g and exp <= e.ts and "expiry" not in flags:
                        return "guard"
                    s["pend"].pop(e.a["of"])
                    s["posted"] -= c
                    return [("put", k, "pend", e.a["of"], (c, exp)), ("add", k, "posted", -c)]
            return "guard"
        if ent not in st:
            return "unknown"
        s = st[ent]
        c = e.a["c"]
        if e.kind == "deposit":
            s["posted"] += c
            return [("add", ent, "posted", c)]
        if e.kind == "fee":
            s["posted"] -= c
            return [("add", ent, "posted", -c)]
        if e.kind in ("auth", "transfer"):
            if g and c > self.avail(s, e.ts, flags):
                return "guard"
            if e.kind == "transfer":
                s["posted"] -= c
                return [("add", ent, "posted", -c)]
            aid = e.eid if e.eid not in s["pend"] else f"{e.eid}#{e.idx}"
            s["pend"][aid] = (c, e.ts + timedelta(hours=W.params["lapse"]))
            return [("pop", ent, "pend", aid)]
        raise ValueError(e.kind)

    def moves(self, st, W, ent, t, rng, mode):
        if ent not in st:
            return [("deposit", {"c": rng.randint(20, 900) * 100}, self.SRC["deposit"])]
        s = st[ent]
        av = self.avail(s, t, frozenset())

        def amt(lo, hi):
            return rng.randint(lo, max(lo, hi)) * 100 + rng.choice([0, 0, 50, 99, 25])

        if mode == "guard":
            out = [("transfer", {"c": max(av, 0) + amt(1, 300)}, self.SRC["transfer"]),
                   ("auth", {"c": max(av, 0) + amt(1, 200)}, self.SRC["auth"])]
            lapsed = [a for a, (c, exp) in s["pend"].items() if exp <= t and "#" not in a]
            if lapsed:
                out.append(("post", {"of": rng.choice(sorted(lapsed)), "_ent": ent}, self.SRC["post"]))
            return out
        out = [("deposit", {"c": amt(10, 900)}, self.SRC["deposit"]),
               ("fee", {"c": rng.choice([250, 500, 999, 1500])}, self.SRC["fee"])]
        if av > 1000:
            out += [("auth", {"c": min(av, amt(5, av // 100))}, self.SRC["auth"]),
                    ("transfer", {"c": min(av, amt(5, av // 100))}, self.SRC["transfer"])]
        if mode == "expiry":
            return [x for x in out if x[0] == "auth"] or out[:1]
        live = [a for a, (c, exp) in s["pend"].items() if exp > t and "#" not in a]
        if live:
            out.append(("post", {"of": rng.choice(sorted(live)), "_ent": ent}, self.SRC["post"]))
        return out

    def expiring(self, W):
        return any(e.kind == "auth" and e.ts <= W.t_q for e in W.events)

    def observe(self, st, W, flags):
        out = {}
        for k in W.ents:
            out[("posted", k)] = st[k]["posted"]
            out[("avail", k)] = self.avail(st[k], W.t_q, flags)
        return out

    def rules(self, W):
        P = W.params
        return ([f"Amounts are in {P['cur']}. The posted balance changes with deposits, fees, transfers and posted "
                 "authorisations. The available balance is the posted balance minus the authorisations still "
                 "pending.",
                 f"A card authorisation is allowed only if its amount is at most the available balance at that "
                 f"moment. It stays pending until it is posted, and it lapses {P['lapse']} hours after it was made (it "
                 "no longer counts at exactly that time).",
                 "A post names the event id of an authorisation that is still pending and not lapsed: its amount "
                 "leaves the posted balance and it stops being pending. Any other post changes nothing.",
                 "A transfer out is allowed only if its amount is at most the available balance at that moment. "
                 "Deposits and fees are always applied.",
                 "Language lines map to the same steps: credited or incoming payment is a deposit, card authorisation "
                 "or merchant hold is an authorisation, posted or settled is a post, fee or service charge is a fee, "
                 "transfer sent or paid out is a transfer out, and a reversal line is a revert."]
                + self.common_rules(W))

    def start_rows(self, W):
        return [(k, [("holder", v["holder"]), ("posted balance", money(v["posted"], W.params["cur"])),
                     ("pending", "none")]) for k, v in W.ents.items()]

    def context(self, W):
        return [("system", "account ledger"), ("currency", W.params["cur"])]

    def label(self, key, W):
        return f"{key[1]} posted balance" if key[0] == "posted" else f"{key[1]} available balance"

    def vtext(self, key, v, W):
        return money(v, W.params["cur"])

    def domain(self, W, q):
        return None

    def option_defs(self, q, opts):
        return None

    VALUE_TPL = {"led.v.a": "What is the posted balance of account {e} {when}, under the numbered rules?",
                 "led.v.b": "Under the ledger rules, which posted balance does account {e} show {when}?"}
    SCORE_TPL = {"led.sc.a": "Which band does the available balance of account {e} fall in {when}?",
                 "led.sc.b": "Under the ledger rules, in which band is the available balance of {e} {when}?"}
    YN = {"ge": {"q": {"led.ge.a": "Is the available balance of account {e} at least {s} {when}?",
                       "led.ge.b": "Under the numbered rules, does account {e} have {s} or more available {when}?"},
                 "neg": {"led.gen.a": "Is the available balance of account {e} below {s} {when}?"},
                 "card": {"yes": "Under the rules the available balance (posted minus pending authorisations) at the "
                                 "stated time is at least the named amount.",
                          "no": "The available balance at the stated time is below the named amount."},
                 "ncard": {"yes": "The available balance at the stated time is below the named amount.",
                           "no": "Under the rules the available balance at the stated time is at least the named "
                                 "amount."},
                 "jb": ("Account {e} has at least {s} available {when}.",
                        "Account {e} has less than {s} available {when}.")}}

    def queries(self, W, qtype, rng):
        if qtype in ("value", "judge"):
            return [Query(qtype, "posted", ("posted", W.target))]
        if qtype == "yn":
            return [Query("yn", "ge", ("avail", W.target))]
        return [Query("score", "band", ("avail", W.target))]

    def pred(self, W, q, v):
        return v >= q.arg

    def levels(self, W, q):
        return [f"{x} {W.params['cur']}" for x in self.LEVELS]

    def level(self, W, q, obs):
        v = obs[q.key]
        return sum(1 for b in self.BOUNDS if v >= b)

    def qfields(self, W, q):
        return {"e": W.target, "s": money(q.arg, W.params["cur"]) if q.arg is not None else None}


# ================================================================================================ F3.7 dialogue slots
class Dialogue(Machine):
    """A customer chat that fills booking slots. Every message maps to one typed update (or none): the customer's own
    requests set values; 'same as before' = the most recent confirmed value of that slot; 'not X' removes X from the
    allowed values; the assistant's confirmation counts only when it repeats the current value; proposals and other
    people's wishes change nothing; a message about another booking reference changes nothing for this one."""
    name, noun, plural, ent_prefix = "dialogue", "booking", "bookings", "BK-"
    gap = (1, 5)
    has_revert = False
    end_phrase = "at the end of the chat"
    SCHEMAS = {"rail": {"seat": ("window", "aisle", "table seat"), "coach": ("coach A", "coach B", "coach C", "coach D"),
                        "meal": ("standard meal", "vegetarian meal", "vegan meal", "no meal")},
               "dinner": {"area": ("terrace", "main room", "bar counter", "private room"),
                          "time": ("18:00", "18:30", "19:00", "19:30", "20:00"),
                          "menu": ("set menu", "a la carte", "tasting menu")},
               "delivery": {"window": ("morning", "midday", "afternoon", "evening"),
                            "drop point": ("front door", "reception", "parcel locker", "neighbour"),
                            "packaging": ("standard box", "gift wrap", "plain bag")}}
    SRC = {"Customer": "Customer", "Assistant": "Assistant"}
    TXT = {"set": ("", ("I'd like the {slot} to be {v}, please.", "Please set the {slot} to {v}.",
                        "Can you make the {slot} {v}?")),
           "oset": ("", ("For my other booking {e}, please set the {slot} to {v}.",
                         "On booking {e} I want the {slot} changed to {v}.")),
           "confirm": ("", ("Confirmed: the {slot} is {v}.", "Done - the {slot} is now {v}.")),
           "same": ("", ("Actually, keep the {slot} the same as before.", "Let's go back to the {slot} we had before.")),
           "not": ("", ("Not the {v}, please.", "Anything but {v} for the {slot}.")),
           "propose": ("", ("Would you like the {slot} to be {v}?", "Shall I switch the {slot} to {v}?")),
           "decline": ("", ("No, thanks.", "No, leave it.")),
           "third": ("", ("My colleague {who} would prefer {v} for the {slot}.",
                          "{who} says the {slot} should be {v}."))}

    def new_eid(self, rng, used):
        return ident(rng, "M", 3, used)

    def other_ent(self, W, rng):
        return W.target

    def new_world(self, rng, pool, spec):
        used = set()
        ids = self.ent_ids(rng, 1, used)
        sch = rng.choice(sorted(self.SCHEMAS))
        slots = self.SCHEMAS[sch]
        conf = {s: rng.choice(vs) for s, vs in slots.items()}
        ents = {ids[0]: {"schema": sch, "confirmed": conf}}
        W = base_world(self, rng, pool, spec, ents, ids[0])
        W.params = {"schema": sch, "slots": {s: list(v) for s, v in slots.items()}, "qslot": rng.choice(sorted(slots)),
                    "customer": pool.person(rng), "colleague": pool.first_name(rng)}
        W.offsets = {"Customer": 0, "Assistant": 0}
        W.ts_style = "iso"
        if spec.traps.get("decoy"):
            self.add_decoy(rng, W, used, False)
        return W

    def init(self, W):
        P = W.params
        c = W.ents[W.target]["confirmed"]
        return {W.target: {s: {"cur": c[s], "conf": [c[s]], "allowed": list(P["slots"][s])} for s in P["slots"]},
                "_": {}}

    def apply(self, st, e, ent, W, flags):
        g = "guards" not in flags
        k = e.kind
        if k == "decline":
            return []
        if k == "oset":
            if ent not in st or ent == "_":
                return "unknown"
            k = "set"
        if k in ("propose", "third") and g:
            return "guard"
        if ent not in st or ent == "_":
            return "unknown"
        S = st[ent][e.a["slot"]]
        old = (S["cur"], list(S["conf"]), list(S["allowed"]))
        if k in ("set", "propose", "third"):
            if g and e.a["v"] not in S["allowed"]:
                return "guard"
            S["cur"] = e.a["v"]
        elif k == "confirm":
            if g and e.a["v"] != S["cur"]:
                return "guard"
            S["conf"].append(e.a["v"])
        elif k == "same":
            if not S["conf"]:
                return "guard"
            S["cur"] = S["conf"][-1]
        elif k == "not":
            if e.a["v"] not in S["allowed"]:
                return "guard"
            S["allowed"].remove(e.a["v"])
            if S["cur"] == e.a["v"] or S["cur"] is None:
                S["cur"] = S["allowed"][0] if len(S["allowed"]) == 1 else None
        else:
            raise ValueError(k)
        return [("put", ent, e.a["slot"], "cur", old[0]), ("put", ent, e.a["slot"], "conf", old[1]),
                ("put", ent, e.a["slot"], "allowed", old[2])]

    def moves(self, st, W, ent, t, rng, mode):
        P = W.params
        slot = P["qslot"] if (mode in ("main", "guard", "after", "expiry") and rng.random() < 0.8) else \
            rng.choice(sorted(P["slots"]))
        if ent not in st or ent == "_":  # another booking reference
            return [("oset", {"slot": slot, "v": rng.choice(P["slots"][slot])}, "Customer")]
        S = st[ent][slot]
        others = [v for v in S["allowed"] if v != S["cur"]]
        if mode == "guard":
            out = []
            if others:
                out.append(("propose", {"slot": slot, "v": rng.choice(others)}, "Assistant"))
                out.append(("third", {"slot": slot, "v": rng.choice(others), "who": P["colleague"]}, "Customer"))
                out.append(("confirm", {"slot": slot, "v": rng.choice(others)}, "Assistant"))
            return out
        out = []
        if others:
            out.append(("set", {"slot": slot, "v": rng.choice(others)}, "Customer"))
        if S["cur"] is not None and S["cur"] != (S["conf"][-1] if S["conf"] else None):
            out.append(("confirm", {"slot": slot, "v": S["cur"]}, "Assistant"))
            if S["conf"]:
                out.append(("same", {"slot": slot}, "Customer"))
        if len(S["allowed"]) > 2 and others and rng.random() < 0.4:
            out.append(("not", {"slot": slot, "v": rng.choice(others)}, "Customer"))
        return out or [("decline", {"slot": slot}, "Customer")]

    def observe(self, st, W, flags):
        return {("slot", s): st[W.target][s]["cur"] for s in W.params["slots"]}

    def rules(self, W):
        P = W.params
        vals = "; ".join(f"{s}: {', '.join(v)}" for s, v in P["slots"].items())
        return ([f"Slots and their allowed values: {vals}.",
                 f"Only the customer's own requests about booking {W.target} change its slots. A request with no "
                 "booking reference is about this booking. The assistant's proposals, the customer's 'no' to a "
                 "proposal, and what other people want change nothing.",
                 "A confirmation by the assistant counts only when it repeats the slot's current value; it makes that "
                 "value the slot's most recent confirmed value. Any other confirmation changes nothing.",
                 "'Same as before' (or 'go back to what we had before') sets the slot to its most recent confirmed "
                 "value.",
                 "'Not X' (or 'anything but X') removes X from the slot's allowed values. If X was the current value, "
                 "or the slot had no value, the slot then takes the only remaining allowed value when exactly one "
                 "remains; otherwise it has no value. A request for a value that is not allowed changes nothing.",
                 "The starting state lists the confirmed values from before this chat; they count as confirmed.",
                 "Messages take effect in timestamp order. A message id that already took effect changes nothing "
                 "when it appears again.",
                 f"Booking references must match character for character; a message about any other reference "
                 f"changes nothing for {W.target}."])

    def start_rows(self, W):
        c = W.ents[W.target]["confirmed"]
        return [(W.target, [(s, v) for s, v in c.items()])]

    def context(self, W):
        return [("system", f"{W.params['schema']} booking chat"), ("customer", W.params["customer"])]

    def label(self, key, W):
        return f"booking {W.target} {key[1]}"

    def vtext(self, key, v, W):
        return v

    def last_event(self, W, key):
        v = None
        for e in time_order(W):
            if e.ts <= W.t_q and e.a.get("slot") == key[1] and "v" in e.a and e.kind != "not":
                v = e.a["v"]
        return v

    def domain(self, W, q):
        return list(W.params["slots"][q.key[1]])

    def option_defs(self, q, opts):
        return None

    def text(self, e, W):
        s, ls = self.TXT[e.kind]
        f = dict(e.a)
        f["e"] = e.ent
        return ls[e.lt % len(ls)].format(**f)

    VALUE_TPL = {"dlg.v.a": "What is the {slot} of booking {e} {when}, under the numbered rules?",
                 "dlg.v.b": "Under the chat rules, which {slot} does booking {e} have {when}?"}
    SCORE_TPL = {}
    REFS = {"same as before": "the most recent confirmed value of that slot (values confirmed before the chat count)",
            "not X": "removes X from the slot's allowed values; if X was the slot's value, or it had none, the slot "
                     "takes the only remaining allowed value when exactly one remains, otherwise it has no value"}
    YN = {"eq": {"q": {"dlg.eq.a": "Is the {slot} of booking {e} {s} {when}?",
                       "dlg.eq.b": "Under the numbered rules, does booking {e} have {s} as its {slot} {when}?"},
                 "neg": {"dlg.eqn.a": "Is the {slot} of booking {e} something other than {s} {when}?"},
                 "card": {**REFS,
                          "yes": "Replaying the chat under the numbered rules, the slot named in the question has "
                                 "exactly the named value at the stated time.",
                          "no": "Under the rules that slot has a different value at the stated time."},
                 "ncard": {**REFS,
                           "yes": "Under the rules the slot named in the question has a value other than the named "
                                  "one at the stated time.",
                           "no": "Replaying the chat under the rules, that slot has exactly the named value then."},
                 "jb": ("The {slot} of booking {e} is {s} {when}.", "The {slot} of booking {e} is not {s} {when}.")}}

    def queries(self, W, qtype, rng):
        k = ("slot", W.params["qslot"])
        if qtype in ("value", "judge", "yn"):
            return [Query(qtype if qtype != "yn" else "yn", "eq" if qtype == "yn" else "slot", k)]
        return []

    def pred(self, W, q, v):
        return v == q.arg

    def qfields(self, W, q):
        return {"e": W.target, "s": q.arg, "slot": W.params["qslot"]}

    def expiring(self, W):
        return False


# ================================================================================================ F3.8 agent trajectories
class Agent(Machine):
    """An assistant's tool calls on a shopping cart or a file store. The tool result on each line says which parts
    succeeded; only successful parts change anything; a batch can partly fail; a retry of a call id takes effect once;
    an undo call reverses the successful parts of the call it names."""
    name, noun, plural = "agent", "item", "items"
    gap = (1, 8)
    end_phrase = "at the end of the session"
    SRC = {"tool": "assistant", "revert": "assistant"}
    FOLDERS = ("inbox", "archive", "shared", "reports", "trash")

    def mentions(self, e):
        if e.kind == "revert":
            return {e.ent}
        return {p[0] for p in e.a["parts"]}

    def guard_present(self, W, out):
        return any(e.kind != "revert" and any(not p[3] and p[0] in W.ents for p in e.a["parts"])
                   for e in W.events if e.ts <= W.t_q)

    def new_eid(self, rng, used):
        return ident(rng, "C", 3, used)

    def new_world(self, rng, pool, spec):
        used = set()
        dom = rng.choice(["cart", "files"])
        n = spec.n_ent or rng.randint(2, 4)
        if dom == "cart":
            ids = [ident(rng, "SKU-", 6, used) for _ in range(n)]
            ents = {x: {"qty": rng.choice([0, 0, 1, 2])} for x in ids}
        else:
            ids = []
            while len(ids) < n:
                x = f"{rng.choice(['report', 'invoice', 'plan', 'notes', 'budget'])}-{rng.randint(1000, 9999)}.pdf"
                body = x.split("-")[1][:4]
                if x not in ids and any(body[i] != body[i + 1] for i in range(3)):
                    ids.append(x)
            used.update(ids)
            ents = {x: {"where": rng.choice(["inbox", "shared", "reports"])} for x in ids}
        W = base_world(self, rng, pool, spec, ents, ids[0])
        W.params = {"dom": dom, "user": pool.person(rng)}
        W.offsets = {"assistant": 0}
        if spec.traps.get("decoy"):
            self.add_decoy(rng, W, used, rng.random() < 0.6, dict(ents[ids[0]]))
        return W

    def init(self, W):
        f = "qty" if W.params["dom"] == "cart" else "where"
        return {k: {f: v[f]} for k, v in W.ents.items()}

    def apply(self, st, e, ent, W, flags):
        g = "guards" not in flags
        parts = e.a["parts"]  # [(ent, op, arg, ok)]
        undo = []
        did = False
        for pe, op, arg, ok in parts:
            if not ok and g:
                continue
            x = W.decoys.get(pe, pe) if "fuzzy" in flags else pe
            if x not in st:
                continue
            s = st[x]
            if op == "add":
                undo.append(("sub0", x, "qty", arg))
                s["qty"] += arg
            elif op == "remove":
                r = min(arg, s["qty"])
                undo.append(("add", x, "qty", -r))
                s["qty"] -= r
            elif op == "set":
                undo.append(("set", x, "qty", s["qty"]))
                s["qty"] = arg
            elif op in ("move", "delete", "restore"):
                undo.append(("set", x, "where", s["where"]))
                s["where"] = arg
            did = True
        return undo if did else "guard"

    def _call(self, W, parts, batch):
        dom = W.params["dom"]
        return parts

    def moves(self, st, W, ent, t, rng, mode):
        dom = W.params["dom"]
        if ent is None:
            ent = W.target
        ok = mode != "guard"
        if dom == "cart":
            cur = st[ent]["qty"] if ent in st else 0
            ops = [("add", rng.randint(1, 3)), ("set", rng.randint(0, 4))] + ([("remove", rng.randint(1, cur))]
                                                                            if cur else [])
            op, arg = pick(rng, ops)
        else:
            cur = st[ent]["where"] if ent in st else "inbox"
            op = "delete" if (cur != "trash" and rng.random() < 0.25) else ("restore" if cur == "trash" else "move")
            arg = "trash" if op == "delete" else ("inbox" if op == "restore" else
                                                   rng.choice([f for f in self.FOLDERS if f not in (cur, "trash")]))
        parts = [(ent, op, arg, ok)]
        if rng.random() < 0.3 and len(W.ents) > 1:  # a batch call: other items, and on a guard slot some succeed
            others = [x for x in W.ents if x != ent]
            for x in rng.sample(others, min(len(others), rng.randint(1, 2))):
                if dom == "cart":
                    parts.append((x, "add", rng.randint(1, 3), rng.random() < 0.7))
                else:
                    parts.append((x, "move", rng.choice(["archive", "reports", "shared"]), rng.random() < 0.7))
            rng.shuffle(parts)
        if mode != "guard" and len(parts) > 1 and all(p[3] for p in parts) and rng.random() < 0.5:
            i = next(j for j, p in enumerate(parts) if p[0] != ent)
            parts[i] = parts[i][:3] + (False,)
        if mode == "guard" and len(parts) > 1:
            if all(not p[3] for p in parts):
                i = next(j for j, p in enumerate(parts) if p[0] != ent)
                parts[i] = parts[i][:3] + (True,)
        return [("call", {"parts": parts, "_ent": ent}, "assistant")]

    def text(self, e, W):
        if e.kind == "revert":
            return f"cart.undo(call={e.a['of']}) -> ok" if W.params["dom"] == "cart" else \
                f"files.undo(call={e.a['of']}) -> ok"
        parts = e.a["parts"]
        dom = W.params["dom"]

        def one(p):
            x, op, arg, ok = p
            if dom == "cart":
                return f"{x} x{arg}" if op in ("add", "remove") else f"{x} to {arg}"
            return x if op in ("delete", "restore") else f"{x} to {arg}"

        if len(parts) == 1:
            x, op, arg, ok = parts[0]
            if dom == "cart":
                call = {"add": f"cart.add(sku={x}, qty={arg})", "remove": f"cart.remove(sku={x}, qty={arg})",
                        "set": f"cart.set_quantity(sku={x}, qty={arg})"}[op]
            else:
                call = {"move": f"files.move(path={x}, folder={arg})", "delete": f"files.delete(path={x})",
                        "restore": f"files.restore(path={x})"}[op]
            res = "ok" if ok else rng_err(e)
            return f"{call} -> {res}"
        op = parts[0][1]
        fn = {"add": "cart.add_many", "remove": "cart.remove_many", "set": "cart.set_many", "move": "files.move_many",
              "delete": "files.delete_many", "restore": "files.restore_many"}
        same = all(p[1] == op for p in parts)
        if not same:
            fn_name = "cart.update_many" if dom == "cart" else "files.update_many"
            items = ", ".join(f"{p[1]} {one(p)}" for p in parts)
        else:
            fn_name = fn[op]
            items = ", ".join(one(p) for p in parts)
        if all(p[3] for p in parts):
            res = "ok"
        elif not any(p[3] for p in parts):
            res = "error: " + rng_err(e).split(": ", 1)[1]
        else:
            res = "partial: " + ", ".join(f"{p[0]} {'ok' if p[3] else 'failed'}" for p in parts)
        return f"{fn_name}({items}) -> {res}"

    def observe(self, st, W, flags):
        f = "qty" if W.params["dom"] == "cart" else "where"
        return {(f, k): st[k][f] for k in W.ents}

    def rules(self, W):
        dom = W.params["dom"]
        base = ["Each line is one tool call by the assistant, with the tool's result after the arrow. Only the parts "
                "the result reports as ok change anything: 'ok' means every part succeeded, 'error' means none did, "
                "and 'partial' lists each part as ok or failed.",
                "A line that repeats a call id is a retry. A call id takes effect at most once: a retry of a call "
                "that already took effect changes nothing.",
                "An undo call names an earlier call id. If that call took effect and has not been undone yet, its "
                "successful parts are undone: quantities it added are taken off again (never below 0), quantities it "
                "removed are put back, and a quantity it set or a file it moved, deleted or restored goes back to "
                "what it was just before that call. Later calls keep their effect. Otherwise the undo changes "
                "nothing.",
                "Calls take effect in timestamp order, whatever order they are listed in.",
                f"Only the {'SKUs' if dom == 'cart' else 'files'} listed in the starting state exist; a call part "
                "naming anything else changes nothing, even when the name looks almost the same.",
                "The state at a stated time counts only the calls timestamped at or before that time."]
        if dom == "cart":
            base.insert(1, "cart.add adds the quantity; cart.remove removes up to the quantity (never below 0); "
                           "cart.set_quantity sets it; the _many and update_many calls do the same per listed item.")
        else:
            base.insert(1, "files.move puts the file in the named folder; files.delete moves it to trash; "
                           "files.restore moves it from trash to inbox; the _many and update_many calls do the same "
                           "per listed file.")
        return base

    def start_rows(self, W):
        f = "qty" if W.params["dom"] == "cart" else "where"
        name = "quantity in cart" if f == "qty" else "folder"
        return [(k, [(name, str(v[f]))]) for k, v in W.ents.items()]

    def context(self, W):
        return [("system", "assistant tool log" + (" - shopping cart" if W.params["dom"] == "cart" else
                                                   " - file store")), ("user", W.params["user"])]

    def label(self, key, W):
        return f"{key[1]} quantity in cart" if key[0] == "qty" else f"{key[1]} folder"

    def vtext(self, key, v, W):
        if key[0] == "qty":
            return f"{v} units" if v != 1 else "1 unit"
        return v

    def last_event(self, W, key):
        v = None
        for e in time_order(W):
            if e.ts > W.t_q or e.kind == "revert":
                continue
            for x, op, arg, ok in e.a["parts"]:
                if x == key[1]:
                    if key[0] == "where":
                        v = arg
                    elif op == "set":
                        v = arg
        return v

    def domain(self, W, q):
        return list(self.FOLDERS) if q.key[0] == "where" else None

    def option_defs(self, q, opts):
        return None

    VALUE_TPL = {"agt.v.a": "{vq} {when}, under the numbered rules?",
                 "agt.v.b": "Under the tool-log rules, {vq2} {when}?"}
    SCORE_TPL = {"agt.sc.a": "{sq} {when}?", "agt.sc.b": "Under the tool-log rules, {sq2} {when}?"}
    YN = {"eq": {"q": {"agt.eq.a": "{yq} {when}?", "agt.eq.b": "Under the numbered rules, {yq2} {when}?"},
                 "neg": {"agt.eqn.a": "{nq} {when}?"},
                 "card": {"yes": "Replaying the tool calls under the numbered rules gives the named value at the "
                                 "stated time.",
                          "no": "Under the rules the value at the stated time is different."},
                 "ncard": {"yes": "Under the rules the value at the stated time differs from the named one.",
                           "no": "Replaying the tool calls under the rules gives exactly the named value then."},
                 "jb": ("{jy} {when}.", "{jn} {when}.")}}

    def queries(self, W, qtype, rng):
        f = "qty" if W.params["dom"] == "cart" else "where"
        k = (f, W.target)
        if qtype in ("value", "judge"):
            return [Query(qtype, f, k)]
        if qtype == "yn":
            return [Query("yn", "eq", k)]
        return [Query("score", "count", None, None, tuple((f, x) for x in W.ents))]

    def pred(self, W, q, v):
        if q.key[0] == "qty":
            return v >= q.arg
        return v == q.arg

    def levels(self, W, q):
        n = len(q.keys)
        if W.params["dom"] == "cart":
            return [f"{i} of the {n} listed items" if i else f"none of the {n} listed items" for i in range(n + 1)]
        return [f"{i} of the {n} listed files" if i else f"none of the {n} listed files" for i in range(n + 1)]

    def level(self, W, q, obs):
        if W.params["dom"] == "cart":
            return sum(1 for k in q.keys if obs.get(k, 0) >= 1)
        return sum(1 for k in q.keys if obs.get(k) == "archive")

    def qfields(self, W, q):
        e, dom = W.target, W.params["dom"]
        s = q.arg
        if dom == "cart":
            f = {"vq": f"How many units of {e} are in the cart", "vq2": f"what quantity of {e} is in the cart",
                 "sq": "How many of the listed items are in the cart (quantity 1 or more)",
                 "sq2": "how many listed items have a quantity of 1 or more in the cart"}
            if s is not None:
                f.update(yq=f"Does the cart hold at least {s} of {e}", yq2=f"is the quantity of {e} in the cart {s} "
                         f"or more", nq=f"Does the cart hold fewer than {s} of {e}",
                         jy=f"The cart holds at least {s} of {e}", jn=f"The cart holds fewer than {s} of {e}")
        else:
            f = {"vq": f"Which folder is {e} in", "vq2": f"which folder holds {e}",
                 "sq": "How many of the listed files are in the archive folder",
                 "sq2": "how many listed files sit in the archive folder"}
            if s is not None:
                f.update(yq=f"Is {e} in the {s} folder", yq2=f"does the {s} folder hold {e}",
                         nq=f"Is {e} somewhere other than the {s} folder", jy=f"{e} is in the {s} folder",
                         jn=f"{e} is not in the {s} folder")
        f.update(e=e, s=s)
        return f

    def expiring(self, W):
        return False


def rng_err(e: Ev) -> str:
    errs = ("error: timeout", "error: item unavailable", "error: permission denied", "error: rate limited")
    return errs[e.lt % len(errs)]


# ================================================================================================ F3.9 flags (held out)
class Flags(Machine):
    name, noun, plural, ent_prefix, ent_digits = "flags", "flag", "flags", "FF-", 4
    rule_style = "b"
    gap = (5, 120)
    has_expiry = True
    SRC = {}
    TXT = {"enable": ("enable flag={e} env={env} change={chg}", ("{by} switched {e} on in {env} ({chg}).",
                                                                  "{e} enabled for {env} under {chg} by {by}.")),
           "disable": ("disable flag={e} env={env} change={chg}", ("{by} switched {e} off in {env} ({chg}).",
                                                                    "{e} disabled for {env} under {chg} by {by}.")),
           "rollout": ("set_rollout flag={e} env={env} percent={p} change={chg}",
                       ("{by} set the {env} rollout of {e} to {p}% ({chg}).",
                        "Rollout of {e} in {env} is now {p}% per {chg}.")),
           "kill": ("kill flag={e}", ("{by} hit the kill switch on {e}.", "Emergency stop engaged for {e} by {by}.")),
           "unkill": ("unkill flag={e} change={chg}", ("{by} cleared the kill switch on {e} ({chg}).",
                                                       "Emergency stop on {e} lifted under {chg} by {by}.")),
           "override": ("override flag={e} user={u} value={val} hours={h}",
                        ("{by} forced {e} {val} for {u} for {h} hours.",
                         "Temporary override: {e} {val} for {u}, {h} hours.")),
           "revert": ("revert event={of}", ("{by} reverted event {of}.", "Undo of event {of} requested by {by}."))}

    def text_fields(self, e, W):
        return {"by": e.src, "chg": e.a.get("chg") or "no change ticket", "val": "on" if e.a.get("on") else "off"}

    def new_world(self, rng, pool, spec):
        used = set()
        n = spec.n_ent or rng.randint(1, 2)
        ids = self.ent_ids(rng, n, used)
        ents = {x: {"enabled": rng.random() < 0.5, "rollout": rng.choice([0, 10, 25, 50])} for x in ids}
        W = base_world(self, rng, pool, spec, ents, ids[0])
        users = []
        while len(users) < 3:
            p = pool.person(rng)
            if p not in users:
                users.append(p)
        eng = []
        while len(eng) < 2:
            p = pool.person(rng)
            if p not in users and p not in eng:
                eng.append(p)
        chg_ok = [f"CHG-{rng.randint(1000, 9999)}" for _ in range(2)]
        chg_bad = f"CHG-{rng.randint(1000, 9999)}"
        W.params = {"users": users, "buckets": {u: rng.randint(0, 99) for u in users}, "user": users[0],
                    "eng": eng, "chg_ok": chg_ok, "chg_bad": chg_bad}
        W.offsets = {p: 0 for p in eng}
        self.mix_offsets(W, rng, spec)
        if spec.traps.get("decoy"):
            self.add_decoy(rng, W, used, rng.random() < 0.6, dict(ents[ids[0]]))
        return W

    def init(self, W):
        return {k: {"enabled": v["enabled"], "rollout": v["rollout"], "killed": False, "ov": {}}
                for k, v in W.ents.items()}

    def apply(self, st, e, ent, W, flags):
        if ent not in st:
            return "unknown"
        s = st[ent]
        g = "guards" not in flags
        k = e.kind
        if k in ("enable", "disable", "rollout", "unkill") and e.a.get("env", "production") == "production":
            if g and e.a.get("chg") not in W.params["chg_ok"]:
                return "guard"
        if k in ("enable", "disable", "rollout") and e.a.get("env") != "production":
            return []
        if k == "enable" or k == "disable":
            old = s["enabled"]
            s["enabled"] = k == "enable"
            return [("set", ent, "enabled", old)]
        if k == "rollout":
            old = s["rollout"]
            s["rollout"] = e.a["p"]
            return [("set", ent, "rollout", old)]
        if k in ("kill", "unkill"):
            old = s["killed"]
            s["killed"] = k == "kill"
            return [("set", ent, "killed", old)]
        if k == "override":
            old = s["ov"].get(e.a["u"])
            s["ov"][e.a["u"]] = (e.a["on"], e.ts + timedelta(hours=e.a["h"]))
            return [("put", ent, "ov", e.a["u"], old)] if old else [("pop", ent, "ov", e.a["u"])]
        raise ValueError(k)

    def on_for(self, s, W, u, flags):
        if s["killed"]:
            return False
        ov = s["ov"].get(u)
        if ov is not None and ("expiry" in flags or ov[1] > W.t_q):
            return ov[0]
        return s["enabled"] and W.params["buckets"][u] < s["rollout"]

    def observe(self, st, W, flags):
        s = st[W.target]
        out = {("on", u): self.on_for(s, W, u, flags) for u in W.params["users"]}
        out[("rollout", W.target)] = s["rollout"]
        return out

    def moves(self, st, W, ent, t, rng, mode):
        P = W.params
        s = st.get(ent)
        by = rng.choice(P["eng"])
        if s is None:
            return [("rollout", {"env": "production", "p": rng.choice([25, 50, 100]), "chg": rng.choice(P["chg_ok"])},
                     by)]
        if mode == "guard":
            return [("rollout", {"env": "production", "p": rng.choice([0, 5, 75, 100]),
                                 "chg": rng.choice([P["chg_bad"], None])}, by),
                    ("enable" if not s["enabled"] else "disable", {"env": "production",
                                                                   "chg": rng.choice([P["chg_bad"], None])}, by)]
        if mode == "expiry":
            return [("override", {"u": P["user"], "on": rng.random() < 0.5, "h": rng.choice([1, 2])}, by)]
        out = [("rollout", {"env": rng.choice(["production", "production", "staging"]),
                            "p": rng.choice([0, 5, 10, 25, 50, 75, 100]), "chg": rng.choice(P["chg_ok"])}, by),
               ("enable" if not s["enabled"] else "disable", {"env": "production", "chg": rng.choice(P["chg_ok"])},
                by),
               ("override", {"u": rng.choice(P["users"]), "on": rng.random() < 0.5, "h": rng.choice([1, 4, 24])},
                by)]
        if rng.random() < 0.2:
            out.append(("kill", {}, by) if not s["killed"] else ("unkill", {"chg": rng.choice(P["chg_ok"])}, by))
        return out

    def expiring(self, W):
        return any(e.kind == "override" and e.ts <= W.t_q for e in W.events)

    def rules(self, W):
        P = W.params
        return (["A flag is on for a person in production when no kill switch is engaged and either an override for "
                 "that person is in force (then the override decides) or the flag is enabled in production and the "
                 "person's bucket number is below the production rollout percentage.",
                 f"Changes to production (enable, disable, rollout, clearing a kill switch) take effect only with an "
                 f"approved change ticket: {', '.join(P['chg_ok'])}. Anything else is rejected and changes nothing. "
                 "Staging changes never affect production.",
                 "Anyone on call may engage a kill switch without a ticket. An override lasts the stated hours from "
                 "its time (it no longer counts at exactly the end time).",
                 "Language lines map to the same steps: switched on or enabled is enable, switched off or disabled is "
                 "disable, set the rollout is rollout, kill switch or emergency stop is kill, cleared or lifted is "
                 "unkill, forced or temporary override is an override, and an undo or revert line is a revert."]
                + self.common_rules(W))

    def start_rows(self, W):
        P = W.params
        rows = [(k, [("production", "enabled" if v["enabled"] else "disabled"), ("rollout", f"{v['rollout']}%"),
                     ("kill switch", "off")]) for k, v in W.ents.items()]
        rows += [(u, [("bucket", str(P["buckets"][u]))]) for u in P["users"]]
        return rows

    def context(self, W):
        return [("system", "feature flag service"), ("environment asked about", "production")]

    def label(self, key, W):
        return f"{W.target} for {key[1]}" if key[0] == "on" else f"{key[1]} production rollout"

    def vtext(self, key, v, W):
        return ("on" if v else "off") if key[0] == "on" else f"{v}%"

    def last_event(self, W, key):
        v = None
        for e in time_order(W):
            if e.ts > W.t_q or e.ent != W.target:
                continue
            if key[0] == "rollout" and e.kind == "rollout":
                v = e.a["p"]
        return v

    def domain(self, W, q):
        return None

    def option_defs(self, q, opts):
        return None

    LEVELS = ("0%", "1% to 24%", "25% to 49%", "50% to 99%", "100%")
    VALUE_TPL = {"flg.v.a": "What is the production rollout percentage of {e} {when}, under the numbered rules?",
                 "flg.v.b": "Under the flag rules, which production rollout does {e} have {when}?"}
    SCORE_TPL = {"flg.sc.a": "Which band is the production rollout of {e} in {when}?",
                 "flg.sc.b": "Under the flag rules, in which rollout band is {e} for production {when}?"}
    YN = {"on": {"q": {"flg.on.a": "Is {e} on for {u} in production {when}?",
                       "flg.on.b": "Under the numbered rules, does {u} get {e} in production {when}?"},
                 "neg": {"flg.onn.a": "Is {e} off for {u} in production {when}?"},
                 "card": {"yes": "Under the rules the flag is on for the named person in production at the stated "
                                 "time.",
                          "no": "Under the rules the flag is off for that person in production at the stated time."},
                 "ncard": {"yes": "Under the rules the flag is off for the named person in production at the stated "
                                  "time.",
                           "no": "Under the rules the flag is on for that person in production at the stated time."},
                 "jb": ("{e} is on for {u} in production {when}.", "{e} is off for {u} in production {when}.")}}

    def queries(self, W, qtype, rng):
        if qtype in ("value", "judge"):
            return [Query(qtype, "rollout", ("rollout", W.target))]
        if qtype == "yn":
            return [Query("yn", "on", ("on", W.params["user"]))]
        return [Query("score", "band", ("rollout", W.target))]

    def pred(self, W, q, v):
        return bool(v)

    def levels(self, W, q):
        return list(self.LEVELS)

    def level(self, W, q, obs):
        v = obs[q.key]
        return 0 if v == 0 else 1 if v < 25 else 2 if v < 50 else 3 if v < 100 else 4

    def qfields(self, W, q):
        return {"e": W.target, "u": W.params["user"]}


# ================================================================================================ F3.10 docs (held out)
class Docs(Machine):
    name, noun, plural, ent_prefix, ent_digits = "docs", "document", "documents", "DOC-", 6
    rule_style = "b"
    gap = (3, 50)
    has_expiry = True
    has_revert = False
    SRC = {}
    LABELS = ("pricing draft", "legal review copy", "summer edition", "board version", "short summary",
              "annotated copy", "final wording", "translator's draft")
    TXT = {"save": ("save doc={e} content=\"{lab}\"", ("{by} saved a new version of {e}: \"{lab}\".",
                                                        "New version of {e} uploaded by {by} (\"{lab}\").")),
           "lock": ("lock doc={e}", ("{by} locked {e} for editing.", "{e} checked out by {by}.")),
           "unlock": ("unlock doc={e}", ("{by} unlocked {e}.", "{e} checked back in by {by}.")),
           "restore": ("restore doc={e} version={k}", ("{by} restored version {k} of {e} as a new version.",
                                                       "{e}: version {k} brought back by {by}.")),
           "approve": ("approve doc={e} version={k}", ("{by} approved version {k} of {e}.",
                                                       "Version {k} of {e} signed off by {by}."))}

    def text_fields(self, e, W):
        return {"by": e.src}

    def new_world(self, rng, pool, spec):
        used = set()
        n = spec.n_ent or rng.randint(1, 2)
        ids = self.ent_ids(rng, n, used)
        labs = list(self.LABELS)
        ents = {x: {"v1": rng.choice(labs)} for x in ids}
        W = base_world(self, rng, pool, spec, ents, ids[0])
        people = []
        while len(people) < 4:
            p = pool.person(rng)
            if p not in people:
                people.append(p)
        W.params = {"editors": people[:3], "approvers": people[1:2] + people[3:4], "lock_min": rng.choice([60, 90, 120])}
        W.offsets = {p: 0 for p in people}
        self.mix_offsets(W, rng, spec)
        if spec.traps.get("decoy"):
            self.add_decoy(rng, W, used, rng.random() < 0.6, {"v1": rng.choice(labs)})
        return W

    def init(self, W):
        return {k: {"vers": [v["v1"]], "lock": None, "appr": []} for k, v in W.ents.items()}

    def _lock(self, s, t, flags, W):
        L = s["lock"]
        return L if (L is not None and ("expiry" in flags or L[1] > t)) else None

    def apply(self, st, e, ent, W, flags):
        if ent not in st:
            return "unknown"
        s = st[ent]
        g = "guards" not in flags
        L = self._lock(s, e.ts, flags, W)
        k = e.kind
        if k in ("save", "restore"):
            if g and L is not None and L[0] != e.src:
                return "guard"
            if k == "restore" and not (1 <= e.a["k"] <= len(s["vers"])):
                return "guard"
            lab = e.a["lab"] if k == "save" else s["vers"][e.a["k"] - 1]
            s["vers"].append(lab)
            return [("popv", ent)]
        if k == "lock":
            if g and L is not None:
                return "guard"
            old = s["lock"]
            s["lock"] = (e.src, e.ts + timedelta(minutes=W.params["lock_min"]))
            return [("set", ent, "lock", old)]
        if k == "unlock":
            if g and (L is None or L[0] != e.src):
                return "guard"
            old = s["lock"]
            s["lock"] = None
            return [("set", ent, "lock", old)]
        if k == "approve":
            if g and (e.src not in W.params["approvers"] or not (1 <= e.a["k"] <= len(s["vers"]))):
                return "guard"
            s["appr"].append(e.a["k"])
            return []
        raise ValueError(k)

    def moves(self, st, W, ent, t, rng, mode):
        P = W.params
        s = st.get(ent)
        if s is None:
            return [("save", {"lab": rng.choice(self.LABELS)}, rng.choice(P["editors"]))]
        L = self._lock(s, t, frozenset(), W)
        n = len(s["vers"])
        if mode == "guard":
            out = []
            if L is not None:
                other = [p for p in P["editors"] if p != L[0]]
                out.append(("save", {"lab": rng.choice(self.LABELS)}, rng.choice(other)))
            out.append(("approve", {"k": n}, rng.choice([p for p in P["editors"] if p not in P["approvers"]])))
            return out
        if mode == "expiry":
            return [("lock", {}, rng.choice(P["editors"]))] if L is None else \
                [("save", {"lab": rng.choice(self.LABELS)}, L[0])]
        who = L[0] if L is not None else rng.choice(P["editors"])
        out = [("save", {"lab": rng.choice([x for x in self.LABELS if x != s["vers"][-1]])}, who),
               ("approve", {"k": n}, rng.choice(P["approvers"]))]
        if n >= 2:
            out.append(("restore", {"k": rng.randint(1, n - 1)}, who))
        if L is None:
            out.append(("lock", {}, who))
        elif rng.random() < 0.4:
            out.append(("unlock", {}, L[0]))
        return out

    def expiring(self, W):
        return any(e.kind == "lock" and e.ts <= W.t_q for e in W.events)

    def observe(self, st, W, flags):
        s = st[W.target]
        return {("content", W.target): s["vers"][-1], ("nvers", W.target): len(s["vers"]),
                ("approved", W.target): len(s["vers"]) in s["appr"]}

    def rules(self, W):
        P = W.params
        return (["Each save or restore adds one new version at the end; the current version is the last one. A "
                 "restore of version k adds a new version with the content of version k. Version 1 is the starting "
                 "content.",
                 f"A lock gives one person sole editing for {P['lock_min']} minutes from the lock time (it no longer "
                 "counts at exactly the end time), or until that person unlocks it. While a lock is in force, saves "
                 "and restores by anyone else are rejected, and a new lock is rejected.",
                 f"Only these approvers can approve a version: {', '.join(P['approvers'])}. An approval by anyone "
                 "else, or of a version that does not exist yet, is rejected. The current version is approved when "
                 "an approval names its number.",
                 "Language lines map to the same steps: saved or uploaded is a save, locked or checked out is a lock, "
                 "unlocked or checked back in is an unlock, restored or brought back is a restore, approved or signed "
                 "off is an approval."]
                + self.common_rules(W, revert=False))

    def start_rows(self, W):
        return [(k, [("version 1 content", v["v1"]), ("lock", "none")]) for k, v in W.ents.items()]

    def context(self, W):
        return [("system", "document store"), ("editors", ", ".join(W.params["editors"]))]

    def label(self, key, W):
        return {"content": f"{key[1]} current content", "nvers": f"{key[1]} number of versions",
                "approved": f"{key[1]} current version approved"}[key[0]]

    def vtext(self, key, v, W):
        if key[0] == "approved":
            return "yes" if v else "no"
        if key[0] == "nvers":
            return str(v)
        return v

    def last_event(self, W, key):
        if key[0] != "content":
            return None
        v = None
        for e in time_order(W):
            if e.ts <= W.t_q and e.ent == key[1] and e.kind == "save":
                v = e.a["lab"]
        return v

    def domain(self, W, q):
        return list(self.LABELS)

    def option_defs(self, q, opts):
        return None

    LEVELS = ("1 version", "2 versions", "3 versions", "4 versions", "5 or more versions")
    VALUE_TPL = {"doc.v.a": "Which content is the current version of {e} {when}, under the numbered rules?",
                 "doc.v.b": "Under the document rules, what does the current version of {e} hold {when}?"}
    SCORE_TPL = {"doc.sc.a": "How many versions does {e} have {when}?",
                 "doc.sc.b": "Under the document rules, how many versions of {e} exist {when}?"}
    YN = {"eq": {"q": {"doc.eq.a": "Is the current version of {e} the \"{s}\" content {when}?",
                       "doc.eq.b": "Under the numbered rules, does the current version of {e} hold the \"{s}\" "
                                   "content {when}?"},
                 "neg": {"doc.eqn.a": "Does the current version of {e} hold anything other than the \"{s}\" content "
                                      "{when}?"},
                 "card": {"yes": "Under the rules the document's current version has exactly the named content at "
                                 "the stated time.",
                          "no": "Under the rules its current version has other content at the stated time."},
                 "ncard": {"yes": "Under the rules its current version has other content at the stated time.",
                           "no": "Under the rules the current version has exactly the named content at the stated "
                                 "time."},
                 "jb": ("The current version of {e} is the \"{s}\" content {when}.",
                        "The current version of {e} is not the \"{s}\" content {when}.")},
          "approved": {"q": {"doc.ap.a": "Is the current version of {e} approved {when}?",
                             "doc.ap.b": "Under the numbered rules, has the current version of {e} been approved "
                                         "{when}?"},
                       "neg": {"doc.apn.a": "Is the current version of {e} still unapproved {when}?"},
                       "card": {"yes": "At the stated time an approval that took effect names the current version's "
                                       "number.",
                                "no": "No approval that took effect names the current version's number at the stated "
                                      "time."},
                       "ncard": {"yes": "No approval that took effect names the current version's number at the "
                                        "stated time.",
                                 "no": "At the stated time an approval that took effect names the current version's "
                                       "number."},
                       "jb": ("The current version of {e} is approved {when}.",
                              "The current version of {e} is not approved {when}.")}}

    def queries(self, W, qtype, rng):
        if qtype in ("value", "judge"):
            return [Query(qtype, "content", ("content", W.target))]
        if qtype == "yn":
            return [Query("yn", "eq", ("content", W.target)), Query("yn", "approved", ("approved", W.target))]
        return [Query("score", "nvers", ("nvers", W.target))]

    def pred(self, W, q, v):
        return v == q.arg if q.fam == "eq" else bool(v)

    def levels(self, W, q):
        return list(self.LEVELS)

    def level(self, W, q, obs):
        return min(obs[q.key], 5) - 1

    def qfields(self, W, q):
        return {"e": W.target, "s": q.arg}


MACHINES: dict[str, Machine] = {m.name: m for m in (Orders(), Tickets(), Access(), Inventory(), Bookings(), Ledger(),
                                                     Dialogue(), Agent(), Flags(), Docs())}
