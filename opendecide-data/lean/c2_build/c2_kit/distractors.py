"""c2_kit/distractors.py: answer options from named error models (C2_DATA_SPEC 3.0 "Options", 3.x traps).

Rule (spec 3.0): every wrong option is the output of one named error model. An error model is a function
spec -> answer key that answers the row the way a reader making exactly one named mistake would (first match instead
of the stated precedence, the earlier anchor, day 0 counted as day 1, cents read as dollars ...). It returns None when
the mistake does not apply to the spec. Error models are plain functions of the spec; most families write them as
"solver A with one rule swapped".

Display is drawn before gold (round-1 lesson 4): the option count k is the family's choice and the gold position is
uhash(row_key, k) — a function of the row key only, never of the answer. Distractors are the distinct non-gold
outputs of the models, in a seeded order. Never pads with random values.

Too few distinct wrong answers returns None, and the caller DROPS the spec. It never retries with a smaller k or with
the abstain option forced on: which wrong answers exist depends on the answer (an abstain gold, a gold at the edge of
the error range), so a k or an abstain display chosen after a failed build carries label information (measured: T25
abstain gold 0% at k = 2 and 39% at k = 4). k and the abstain display are drawn once from the row key; a family
whose error models are too thin for its k draws a smaller k for every row, not for the rows that fail.

Ordered answers (dates, counts, amounts; or any visible order, such as option length): pass order_key, and the
gold's sorted RANK among the shown ordered options (the abstain option is not ordered) is drawn from the row key too
(target_rank, uniform over 0..n-1); the distractors are picked so that exactly that many sit below the gold. Without
it a content-free "pick the middle date" rule finds the gold (round-1-style error models put day-0 and one-day-late
misreadings on both sides of it). ordered_k() is the one allowed way to size an ordered set from the spec: min(k, 1 +
the smaller of the two sides' candidate counts), which is the same whatever rank the row draws, so it never moves the
rank. exclusive: groups of model names that never share an option set (two partial sums whose total is the gold
would let "the option that is the sum of two others" find it).

Open answer sets (dates, amounts, rule ids, ...): build_options(). Closed label sets (allow / ask / deny): build_closed()
shows the whole set, records which models produce each wrong label (role "closed" when none does).
Abstain options ("cannot decide", "none"): shown or not by the family's label-blind draw; when gold is the abstain key
it is always shown. abstain_report() checks the spec bar (wrong on >= 50% of the rows that show it) over all rows,
abstain_cells() per (k, abstain shown) cell, where the bar must hold too.

Planned display (c2_kit.choiceplan; pilot lesson: abstain gold far below 1/k in 9 families). Pass plan=ChoicePlan to
build_options / build_closed: k, the abstain display, the gold position and the gold rank come from the plan, which
the sampler drew from the row key BEFORE drawing structure, and the sampler only keeps structures whose gold agrees
with plan.gold_abstain. strict_plan=True (base rows) raises choiceplan.PlanMismatch when the gold disagrees;
strict_plan=False (twins / premise-removal partners) adapts the plan to the constructed gold (plan.for_gold).
length_balance=True orders the non-abstain options by their visible length (then text) and puts the gold at the
planned rank, so gold-is-longest / -shortest are 1/n by construction (the abstain option is not ordered: its
gold share 1/k keeps it balanced). abstain_slot "last" (in the plan) keeps the abstain option as the last option.
Without plan the functions behave exactly as before (same options, same order).
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Callable

CATALOG = {
    "first_match": "takes the first listed matching rule, ignoring the stated precedence",
    "last_match": "takes the last listed matching rule, ignoring the stated precedence",
    "most_specific": "takes the most specific matching rule, ignoring the stated precedence",
    "effect_order": "takes the strongest effect among matches, ignoring the stated precedence",
    "ignore_arguments": "matches on the tool or action name and ignores its argument conditions",
    "default_allow": "falls back to allowing the action when no rule is read as matching",
    "ignore_default": "ignores the stated default for the no-match case",
    "earlier_anchor": "anchors the period on the earlier of two events",
    "wrong_anchor": "anchors the period on another date that appears in the text",
    "count_day0": "counts the anchor day as day 1",
    "off_by_one_late": "counts one day past the end of the period",
    "drop_inclusive_endpoint": "treats an inclusive endpoint as exclusive",
    "add_exclusive_endpoint": "treats an exclusive endpoint as inclusive",
    "more_than_as_at_least": "reads 'more than' as 'at least'",
    "at_least_as_more_than": "reads 'at least' as 'more than'",
    "calendar_year": "uses the calendar year instead of the rolling window",
    "wrong_roll_direction": "rolls the window forward instead of back (or back instead of forward)",
    "netting": "nets cash-in against cash-out",
    "skip_offset_conversion": "compares clock times without converting their UTC offsets",
    "newest_version": "applies the newest version whatever the transition clause says",
    "status_word": "trusts a success word or 2xx code on an unfinished or failed step",
    "cents_as_dollars": "reads an amount in cents as dollars",
    "stop_at_first_gate": "stops at the first gate and ignores later gates or routes",
    "net_vs_gross": "uses net where the rule says gross (or the reverse)",
    "wrong_tiebreak": "applies the tie-breakers in the wrong order",
    "ignore_exception": "ignores a stated exception",
    "ignore_qualifier": "reads the headline promise and ignores its qualifier",
    "ignore_revocation": "ignores a revocation or override",
    "ignore_scope": "ignores the user's scope and follows the embedded request",
    "lookalike_domain": "accepts a look-alike domain as the registered one",
    "first_failure_only": "reports the first failing check in listed order, not the stated check order",
}


def register_name(name: str, describe: str) -> None:
    """A family-specific error-model name (recorded in its G0-lite spec)."""
    if name in CATALOG and CATALOG[name] != describe:
        raise ValueError(f"error model {name!r} already means: {CATALOG[name]}")
    if not describe.strip():
        raise ValueError("an error model needs a description")
    CATALOG[name] = describe


@dataclass(frozen=True)
class ErrorModel:
    name: str
    fn: Callable[[Any], Any]
    describe: str = ""

    def __post_init__(self):
        if self.name not in CATALOG and not self.describe:
            raise ValueError(f"error model {self.name!r}: not in CATALOG and no description")

    @property
    def text(self) -> str:
        return self.describe or CATALOG[self.name]


def error_model(name: str, fn: Callable, describe: str = "") -> ErrorModel:
    return ErrorModel(name, fn, describe)


@dataclass(frozen=True)
class Option:
    key: Any
    text: str
    role: str                    # gold | error | abstain | closed
    err: tuple = ()              # error models that produce this option


@dataclass
class OptionSet:
    options: list
    gold_index: int
    meta: dict = field(default_factory=dict)

    @property
    def texts(self) -> list:
        return [o.text for o in self.options]

    @property
    def gold(self) -> Option:
        return self.options[self.gold_index]

    @property
    def opt_err(self) -> dict:
        """{option text: [error model, ...]} for row meta (spec 3.0 provenance of every wrong option)."""
        return {o.text: list(o.err) for o in self.options if o.role != "gold"}

    @property
    def abstain_shown(self) -> bool:
        return any(o.role == "abstain" or (o.role == "gold" and self.meta.get("gold_is_abstain")) for o in self.options)


def uhash(*parts) -> float:
    h = hashlib.sha256("\x1f".join(str(p) for p in parts).encode()).digest()
    return int.from_bytes(h[:8], "big") / 2 ** 64


def gold_position(row_key: str, k: int) -> int:
    """Label-blind: depends on the row key and the option count only."""
    return min(k - 1, int(uhash(row_key, "gold_pos", k) * k))


def target_rank(row_key: str, k: int) -> int:
    """Label-blind sorted rank of the gold among k ordered options (0 = smallest): row key and k only."""
    return min(k - 1, int(uhash(row_key, "gold_rank", k) * k))


def _norm(t: str) -> str:
    return " ".join(t.casefold().split())


def _groups_of(names, exclusive) -> set:
    return {i for i, g in enumerate(exclusive) if set(g) & set(names)}


def _sides(wrong: dict, gold, order_key: Callable, exclusive) -> tuple:
    """(below, above): how many options each side of the gold can hold (a group of exclusive models counts once)."""
    g0 = order_key(gold)
    out = []
    for side in (lambda a: order_key(a) < g0, lambda a: order_key(a) > g0):
        free = [a for a in wrong if side(a) and not _groups_of(wrong[a], exclusive)]
        grouped = set().union(*([_groups_of(wrong[a], exclusive) for a in wrong if side(a)] or [set()]))
        out.append(len(free) + len(grouped))
    return tuple(out)


def ordered_k(spec, gold, models: dict, *, k: int, order_key: Callable, exclusive: tuple = ()) -> int | None:
    """The option count for an ordered set: min(k, 1 + min(below, above)); None when a side is empty. Symmetric in the
    two sides, so the rank target_rank() then draws for this k stays uniform whatever the gold's place in the error
    range (a side-specific rule would make a high rank fail more often on golds at the top of their range)."""
    below, above = _sides(_run_models(spec, gold, models), gold, order_key, exclusive)
    m = min(below, above)
    return None if m == 0 else min(k, m + 1)


def _run_models(spec, gold, models: dict) -> dict:
    out: dict = {}
    for name in sorted(models):
        m = models[name]
        if m.name != name:
            raise ValueError(f"error model registered as {name!r} is named {m.name!r}")
        ans = m.fn(spec)
        if ans is None or ans == gold:
            continue
        out.setdefault(ans, []).append(name)
    return out


def _length_key(render_key: Callable[[Any], str]) -> Callable[[Any], tuple]:
    """Visible-length order of an option (then its text, so distinct texts never tie)."""
    return lambda a: (len(render_key(a)), render_key(a))


def _adopt_plan(plan, gold, abstain, strict_plan: bool, *, k=None, show_abstain=False):
    """Check a ChoicePlan against the call and the gold; return the plan the row is built with."""
    from .choiceplan import PlanMismatch
    if k is not None and k != plan.k:
        raise ValueError(f"k {k} != plan.k {plan.k} (a planned row takes k from its plan)")
    if show_abstain and not plan.show_abstain:
        raise ValueError("show_abstain comes from the plan")
    if (plan.show_abstain or plan.gold_abstain) and abstain is None:
        raise ValueError("the plan shows an abstain option: pass abstain=(key, text)")
    gia = abstain is not None and gold == abstain[0]
    if gia != plan.gold_abstain:
        if strict_plan:
            raise PlanMismatch(f"gold {gold!r}: abstain gold {gia}, the plan says {plan.gold_abstain} (draw another "
                               f"structure; never relabel)")
        plan = plan.for_gold(gia)
    return plan


def build_options(spec, gold, models: dict, *, k: int | None = None, row_key: str, render_key: Callable[[Any], str],
                  abstain: tuple | None = None, show_abstain: bool = False, order_key: Callable | None = None,
                  exclusive: tuple = (), plan=None, length_balance: bool = False,
                  strict_plan: bool = True) -> OptionSet | None:
    """k options for an open answer set: gold + (k - 1) distinct error-model outputs (+ the abstain option when
    shown). abstain = (key, text). order_key: the answers are ordered and the gold takes the sorted rank
    target_rank(row_key, n) among the n ordered (non-abstain) options; an abstain gold has no rank. exclusive: tuples
    of model names whose outputs never appear together. Returns None when the models give too few distinct wrong
    answers: the caller drops or resamples the spec (module docstring), it never retries with another k or with the
    abstain option forced on.
    plan (choiceplan.ChoicePlan, drawn at sampling time): k, the abstain display, the gold position and rank come
    from it; strict_plan (base rows) raises PlanMismatch when the gold is / is not the abstain key against the plan;
    strict_plan=False (partner rows) adapts the plan to the gold. length_balance: rank the non-abstain options by
    visible length (then text) and put the gold at the planned (or row-key) rank; one order per row, so not with
    order_key."""
    if order_key is not None and length_balance:
        raise ValueError("one order per row: order_key (values) or length_balance (visible length), not both")
    if length_balance:
        order_key = _length_key(render_key)
    slot = "shuffle"
    if plan is not None:
        plan = _adopt_plan(plan, gold, abstain, strict_plan, k=k, show_abstain=show_abstain)
        k, show_abstain, slot = plan.k, plan.show_abstain, plan.abstain_slot
    if k is None or k < 2:
        raise ValueError("k >= 2")
    gold_is_abstain = abstain is not None and gold == abstain[0]
    show = gold_is_abstain or (abstain is not None and show_abstain)
    wrong = _run_models(spec, gold, models)
    if abstain is not None:
        wrong.pop(abstain[0], None)
    if length_balance and not gold_is_abstain:      # a wrong answer that renders as the gold can never be shown
        gt = _norm(render_key(gold))
        wrong = {a: v for a, v in wrong.items() if _norm(render_key(a)) != gt}
    need = k - 1 - (1 if show and not gold_is_abstain else 0)
    order = sorted(wrong, key=lambda a: uhash(row_key, "opt", repr(a)))
    rank = None
    if order_key is None or gold_is_abstain:
        quota = {None: need}
    else:
        rank = plan.rank if (plan is not None and plan.rank is not None) else target_rank(row_key, need + 1)
        quota = {"lo": rank, "hi": need - rank}
        g0 = order_key(gold)
        if any(order_key(a) == g0 for a in wrong):
            raise ValueError("order_key maps a wrong answer onto the gold's place")
    picks, used = [], set()
    for a in order:
        side = None if rank is None else ("lo" if order_key(a) < g0 else "hi")
        gs = _groups_of(wrong[a], exclusive)
        if quota[side] == 0 or gs & used:
            continue
        picks.append(a)
        quota[side] -= 1
        used |= gs
    if any(quota.values()):
        return None
    gold_opt = Option(gold, abstain[1] if gold_is_abstain else render_key(gold), "gold")
    others = [Option(a, render_key(a), "error", tuple(wrong[a])) for a in picks]
    abst = Option(abstain[0], abstain[1], "abstain") if show and not gold_is_abstain else None
    if slot == "last" and show:
        others.sort(key=lambda o: uhash(row_key, "slot", repr(o.key)))
        pos = plan.pos
        opts = others + [gold_opt] if gold_is_abstain else others[:pos] + [gold_opt] + others[pos:] + [abst]
    else:
        if abst is not None:
            others.append(abst)
        others.sort(key=lambda o: uhash(row_key, "slot", repr(o.key)))
        pos = plan.pos if plan is not None else gold_position(row_key, k)
        opts = others[:pos] + [gold_opt] + others[pos:]
    texts = [_norm(o.text) for o in opts]
    if len(set(texts)) != len(texts) or any(not o.text or "\n" in o.text for o in opts):
        return None
    meta = {"kind": "open", "k": k, "gold_is_abstain": gold_is_abstain,
            "abstain_key": abstain[0] if abstain else None, "gold_rank": rank}
    if plan is not None or length_balance:
        meta.update(plan=None if plan is None else plan.to_json(), length_balance=length_balance, abstain_slot=slot)
    return OptionSet(opts, pos, meta)


def build_closed(spec, gold, closed: list, models: dict, *, row_key: str, render_key: Callable[[Any], str],
                 order: str = "shuffle", abstain: tuple | None = None, show_abstain: bool = False, plan=None,
                 strict_plan: bool = True) -> OptionSet:
    """The family's whole closed label set (+ abstain when shown). order "fixed" keeps the card order (the trainer
    shuffles options again at train time); "shuffle" draws a label-blind permutation from the row key.
    plan (choiceplan.plan_choice(row_key, closed=len(closed), abstain=...)): the abstain display and the gold
    position come from the plan (the other labels keep their seeded order); strict_plan as in build_options."""
    if gold not in closed and not (abstain and gold == abstain[0]):
        raise ValueError(f"gold {gold!r} is not in the closed set")
    slot = "shuffle"
    if plan is not None:
        if order != "shuffle":
            raise ValueError("a planned closed set takes its order from the plan (order 'shuffle')")
        plan = _adopt_plan(plan, gold, abstain, strict_plan, show_abstain=show_abstain)
        if plan.k != len(closed) + int(plan.show_abstain):
            raise ValueError(f"plan.k {plan.k} != {len(closed)} labels + abstain shown {plan.show_abstain}")
        show_abstain, slot = plan.show_abstain, plan.abstain_slot
    wrong = _run_models(spec, gold, models)
    keys = list(closed)
    gold_is_abstain = abstain is not None and gold == abstain[0]
    if abstain is not None and (show_abstain or gold_is_abstain):
        keys.append(abstain[0])
    if plan is not None:
        ab = abstain[0] if abstain is not None and abstain[0] in keys and not gold_is_abstain else None
        others = [a for a in keys if a != gold and not (slot == "last" and a == ab)]
        others.sort(key=lambda a: uhash(row_key, "closed", repr(a)))
        if slot == "last" and (ab is not None or gold_is_abstain):
            keys = others + [gold] if gold_is_abstain else others[:plan.pos] + [gold] + others[plan.pos:] + [ab]
        else:
            keys = others[:plan.pos] + [gold] + others[plan.pos:]
    elif order == "shuffle":
        keys.sort(key=lambda a: uhash(row_key, "closed", repr(a)))
    opts = []
    for a in keys:
        if a == gold:
            text = abstain[1] if gold_is_abstain else render_key(a)
            opts.append(Option(a, text, "gold"))
        elif abstain is not None and a == abstain[0]:
            opts.append(Option(a, abstain[1], "abstain"))
        else:
            ms = tuple(wrong.get(a, ()))
            opts.append(Option(a, render_key(a), "error" if ms else "closed", ms))
    gi = keys.index(gold)
    texts = [_norm(o.text) for o in opts]
    if len(set(texts)) != len(texts):
        raise ValueError("closed set renders two options alike")
    meta = {"kind": "closed", "k": len(opts), "gold_is_abstain": gold_is_abstain,
            "abstain_key": abstain[0] if abstain else None}
    if plan is not None:
        meta.update(plan=plan.to_json(), abstain_slot=slot)
    return OptionSet(opts, gi, meta)


def check_named(os_: OptionSet) -> list:
    """Problems: an open-set wrong option without a model, a missing gold, duplicate texts."""
    probs = []
    if os_.options[os_.gold_index].role != "gold" or sum(o.role == "gold" for o in os_.options) != 1:
        probs.append("exactly one gold option at gold_index")
    if os_.meta.get("kind") == "open":
        probs += [f"wrong option {o.text!r} has no error model" for o in os_.options if o.role == "error" and not o.err]
        probs += [f"option {o.text!r} role {o.role}" for o in os_.options if o.role == "closed"]
    if len({_norm(t) for t in os_.texts}) != len(os_.texts):
        probs.append("duplicate option texts")
    return probs


def abstain_report(sets: list) -> dict:
    """Spec 3.0: an abstain option is wrong on >= 50% of the rows that show it."""
    shown = [s for s in sets if s.meta.get("abstain_key") is not None and s.abstain_shown]
    wrong = sum(1 for s in shown if not s.meta.get("gold_is_abstain"))
    share = wrong / len(shown) if shown else None
    return {"rows_showing": len(shown), "abstain_wrong": wrong, "wrong_share": share,
            "pass": share is None or share >= 0.5}


def abstain_cells(sets: list) -> dict:
    """{(k, abstain shown): {"rows", "abstain_gold", "wrong_share"}} for the sets that can show an abstain option. The
    spec 3.0 bar holds in every cell with >= 30 rows, and the abstain-gold share must not move with k (a k chosen
    after a failed build makes it move: module docstring)."""
    out: dict = {}
    for s in sets:
        if s.meta.get("abstain_key") is None:
            continue
        c = out.setdefault((len(s.options), s.abstain_shown), {"rows": 0, "abstain_gold": 0})
        c["rows"] += 1
        c["abstain_gold"] += bool(s.meta.get("gold_is_abstain"))
    for c in out.values():
        c["wrong_share"] = 1 - c["abstain_gold"] / c["rows"]
    return out


def position_counts(sets: list) -> dict:
    """{k: [count of gold at position 0..k-1]} (G10: uniform per option bucket)."""
    out: dict = {}
    for s in sets:
        k = len(s.options)
        out.setdefault(k, [0] * k)[s.gold_index] += 1
    return out


def ordered_cues(sets: list) -> dict:
    """Content-free options-only rules on ordered sets (G6 b pre-check; spec 6.3): for each k, the gold rate of "take
    the option at sorted rank r" (rank_rate[r]) and of "take an option that equals the sum of two others" (sum_rate),
    with chance 1 / k. Keys must sort; the sum rule reads numeric keys only."""
    out: dict = {}
    for s in sets:
        keys = sorted(o.key for o in s.options)
        k = len(keys)
        c = out.setdefault(k, {"rows": 0, "rank_hits": [0] * k, "sum_options": 0, "sum_gold": 0})
        c["rows"] += 1
        c["rank_hits"][keys.index(s.gold.key)] += 1
        for o in s.options:
            rest = [x.key for x in s.options if x is not o]
            if isinstance(o.key, (int, float)) and any(a + b == o.key for i, a in enumerate(rest)
                                                       for b in rest[i + 1:]):
                c["sum_options"] += 1
                c["sum_gold"] += o.role == "gold"
    for k, c in out.items():
        c["chance"] = 1 / k
        c["rank_rate"] = [h / c["rows"] for h in c["rank_hits"]]
        c["sum_rate"] = c["sum_gold"] / c["sum_options"] if c["sum_options"] else None
    return out


def rank_counts(sets: list) -> dict:
    """{n: [count of gold at sorted rank 0..n-1]} over ordered sets, n = the ordered (non-abstain) options shown
    (uniform per option count)."""
    out: dict = {}
    for s in sets:
        r = s.meta.get("gold_rank")
        if r is not None:
            n = len(s.options) - s.abstain_shown
            out.setdefault(n, [0] * n)[r] += 1
    return out
