"""c2_kit/choiceplan.py: the display plan of a choice row, drawn at SAMPLING time from the row key (C2_DATA_SPEC 3.0
"Options" and "Abstain options"; 6.3 G6, G7, G10).

The pilot pattern it fixes (STAGE_B_PILOT_REPORT): the abstain / "none" / "no line matches" option is gold far below
1/k in 9 families (T35 24 of 184 rows against 54 expected; T30 49 of 387 against 129; T36 48 of 331 against 97 ...).
The abstain option is shown on most rows and is usually the longest text, so one fact fails three gates at once:
G6 options-only ("never pick it" beats chance), G7 (the abstain feature) and G10 (gold-is-longest -15 to -17 pp).
The cause is the sampler: it draws the abstain outcome at a fixed rate (T35 15%), not at the rate the display implies.

The plan. Before any structure is drawn, plan_choice(row_key, ...) fixes, from the row key alone (label-blind):
  k              the number of options shown (abstain included when shown)
  show_abstain   whether the abstain option is shown (always when the gold is the abstain key)
  gold_abstain   whether this row's gold IS the abstain option: P = abstain_share(k), default 1/k
  pos            the gold's position (distractors.gold_position; with abstain_slot "last" the abstain option sits last
                 and pos is drawn so that every position is still 1/k)
  rank           the gold's sorted rank among the n = k - show_abstain ordered options (distractors.target_rank),
                 used for the option-LENGTH balance (build_options(length_balance=True)) or a value order (order_key)
The sampler then draws structure until solver A's gold agrees with plan.gold_abstain (label-first: the target is
drawn first, the spec is built to reach it, the gold always comes from solver A) and build_options(plan=plan) fills
the planned k, position and rank. Rejection happens on STRUCTURE under a fixed plan, so the realised rows keep the
plan's marginals: abstain gold 1/k in every (k, shown) cell, gold position uniform, length rank uniform. Nothing is
ever relabelled and no display choice reads the gold.

Why 1/k: with the abstain option shown on a row of k options, the G7 null is "the abstain option is gold 1/k of the
time" (expected count = sum of 1/k), G6's options-only reader can then not use it, and gold-is-longest is 1/k
whether or not the abstain text is the longest (rows with an abstain gold give 1/k * P(abstain longest), the others
(1 - 1/k) * 1/(k - 1) * P(abstain not longest), which sum to 1/k). 1/k <= 1/2 for k >= 2, so spec 3.0's "an abstain
option is wrong on >= 50% of the rows that show it" holds in every cell. A family whose G0 states another share may
pass abstain_share, but any share other than 1/k makes the abstain option predictive in G6 / G7: re-freeze the G0
band to 1/k instead.

Partner rows (twins, premise removal) re-render under the same row key with another gold. Render them with
build_options(plan=..., strict_plan=False): k, display and position stay, the abstain option is shown when the new
gold is the abstain key, and a rank is drawn when the plan had none. plan_report() measures what actually came out.
"""
from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any, Callable

from .distractors import gold_position, target_rank, uhash

ABSTAIN_SLOTS = ("shuffle", "last")


class PlanMismatch(ValueError):
    """A base row's gold disagrees with its plan (the sampler must draw another structure, never relabel)."""


@dataclass(frozen=True)
class ChoicePlan:
    row_key: str
    k: int
    show_abstain: bool
    gold_abstain: bool
    pos: int
    rank: int | None
    abstain_share: float
    abstain_slot: str = "shuffle"
    closed: int | None = None          # closed label sets: the number of labels (k = closed + abstain shown)

    def __post_init__(self):
        if self.k < 2 or not 0 <= self.pos < self.k:
            raise ValueError(f"plan: k {self.k} / pos {self.pos}")
        if self.gold_abstain and not self.show_abstain:
            raise ValueError("plan: an abstain gold is always shown")
        if self.abstain_slot not in ABSTAIN_SLOTS:
            raise ValueError(f"abstain_slot {self.abstain_slot!r}")
        if self.abstain_slot == "last" and self.show_abstain and self.gold_abstain != (self.pos == self.k - 1):
            raise ValueError("plan: with abstain_slot 'last' the abstain option holds the last position")

    @property
    def n_ordered(self) -> int:
        """Options that take part in a rank (the abstain option is not ordered)."""
        return self.k - int(self.show_abstain)

    def accepts(self, gold, abstain_key) -> bool:
        """True when a base row's gold matches the plan (gold is the abstain key exactly when planned)."""
        return (abstain_key is not None and gold == abstain_key) == self.gold_abstain

    def for_gold(self, gold_is_abstain: bool) -> "ChoicePlan":
        """The plan of a partner row whose gold came out of the construction (twin, premise removal): same k, display
        and position; the abstain option shown when the gold is the abstain key; a label-blind rank when needed."""
        if gold_is_abstain == self.gold_abstain:
            return self
        show = self.show_abstain or gold_is_abstain
        k = self.k if self.closed is None else self.closed + int(show)      # an open set keeps k (abstain replaces
        if self.abstain_slot == "last" and show:                             # a distractor); a closed set grows by one
            if gold_is_abstain:
                pos = k - 1
            else:
                pos = min(k - 2, int(uhash(self.row_key, "plan", "pos_last", k) * (k - 1)))
        else:
            pos = self.pos if k == self.k else gold_position(self.row_key, k)
        rank = None if gold_is_abstain else target_rank(self.row_key, k - int(show))
        return ChoicePlan(self.row_key, k, show, gold_is_abstain, pos, rank, self.abstain_share, self.abstain_slot,
                          self.closed)

    def to_json(self) -> dict:
        return asdict(self)

    @classmethod
    def from_json(cls, d: dict) -> "ChoicePlan":
        return cls(**d)


def share_for(k: int, abstain_share=None) -> float:
    """P(gold is the abstain option | k options, abstain shown): 1/k by default; a float; or a function of k."""
    v = (1.0 / k) if abstain_share is None else (abstain_share(k) if callable(abstain_share) else float(abstain_share))
    if not 0.0 <= v <= 0.5:
        raise ValueError(f"abstain share {v} at k = {k}: spec 3.0 needs the abstain option wrong on >= 50% of the "
                         f"rows that show it (share <= 0.5)")
    return v


def _pick(u: float, values: tuple, weights=None) -> Any:
    if weights is None:
        return values[min(len(values) - 1, int(u * len(values)))]
    tot = float(sum(weights))
    acc = 0.0
    for v, w in zip(values, weights):
        acc += w / tot
        if u < acc:
            return v
    return values[-1]


def plan_choice(row_key: str, *, ks=(3, 4), k_weights=None, closed: int | None = None, abstain: bool = False,
                show_rate: float = 1.0, abstain_share=None, abstain_slot: str = "shuffle") -> ChoicePlan:
    """The display plan of one choice row, from the row key only.

    ks / k_weights: open answer sets; k counts every shown option, the abstain option included.
    closed:         closed label sets: the number of labels; k = closed + 1 when the abstain option is shown.
    abstain:        the form can show an abstain option (QuestionForm.abstain); show_rate: the share of rows that
                    show it (1.0: every row); abstain_share: P(gold is abstain | shown), default 1/k.
    abstain_slot:   "shuffle" (the abstain option takes a seeded position like any option) or "last".
    With abstain False, gold_abstain is always False and the plan is the kit's usual label-blind k, position and
    rank (so a family that only wants the length balance passes abstain=False)."""
    if abstain_slot not in ABSTAIN_SLOTS:
        raise ValueError(f"abstain_slot {abstain_slot!r}")
    if not 0.0 <= show_rate <= 1.0:
        raise ValueError("show_rate in [0, 1]")
    if closed is not None:
        if closed < 2:
            raise ValueError("a closed set has >= 2 labels")
        show = abstain and uhash(row_key, "plan", "show", closed) < show_rate
        k = closed + int(show)
    else:
        ks = tuple(ks)
        if not ks or min(ks) < 2 or (k_weights is not None and len(k_weights) != len(ks)):
            raise ValueError("ks: option counts >= 2 (and one weight per count)")
        k = _pick(uhash(row_key, "plan", "k"), ks, k_weights)
        show = abstain and uhash(row_key, "plan", "show", k) < show_rate
    if show and k < 3 and closed is None:
        raise ValueError("an open set that shows the abstain option needs k >= 3 (gold + abstain + 1 error)")
    share = share_for(k, abstain_share) if show else 0.0
    gold_abstain = bool(show and uhash(row_key, "plan", "abstain", k) < share)
    if abstain_slot == "last" and show:
        pos = k - 1 if gold_abstain else min(k - 2, int(uhash(row_key, "plan", "pos_last", k) * (k - 1)))
    else:
        pos = gold_position(row_key, k)
    rank = None if gold_abstain else target_rank(row_key, k - int(show))
    return ChoicePlan(row_key, k, show, gold_abstain, pos, rank, share, abstain_slot, closed)


def realize(plan: ChoicePlan, draw: Callable[[int], Any], *, solve: Callable[[Any], Any], abstain_key=None,
            fits: Callable[[Any, Any], bool] | None = None, tries: int = 400):
    """Draw structure under a fixed plan: draw(attempt) -> spec or None; keep the first spec whose solver-A gold
    agrees with the plan (plan.accepts) and, when given, fits(spec, gold) (e.g. build_options(..., plan=plan) is not
    None). Returns (spec, attempts). Raises PlanMismatch after `tries` attempts: the caller drops the SEED (never the
    plan's cell selectively: a family whose structures cannot reach a cell must change its sampler, not its plan)."""
    for i in range(tries):
        spec = draw(i)
        if spec is None:
            continue
        gold = solve(spec)
        if plan.accepts(gold, abstain_key) and (fits is None or fits(spec, gold)):
            return spec, i + 1
    raise PlanMismatch(f"no structure reached the plan {plan.to_json()} in {tries} attempts")


# ------------------------------------------------------------------------------------------------ report

def _log_binom_pmf(n: int, k: int, p: float) -> float:
    if p <= 0.0:
        return 0.0 if k == 0 else -math.inf
    if p >= 1.0:
        return 0.0 if k == n else -math.inf
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) + k * math.log(p) + (n - k) * math.log1p(-p)


def binom_two_sided(x: int, n: int, p: float) -> float:
    """Exact two-sided binomial p-value (sum of the outcomes no more likely than x)."""
    if n == 0:
        return 1.0
    lx = _log_binom_pmf(n, x, p)
    tot = 0.0
    for j in range(n + 1):
        lj = _log_binom_pmf(n, j, p)
        if lj <= lx + 1e-9:
            tot += math.exp(lj)
    return min(1.0, tot)


def _gammaincc(a: float, x: float) -> float:
    """Regularized upper incomplete gamma Q(a, x) (series / continued fraction)."""
    if x <= 0:
        return 1.0
    if x < a + 1:
        term = s = 1.0 / a
        ap = a
        for _ in range(1000):
            ap += 1
            term *= x / ap
            s += term
            if abs(term) < abs(s) * 1e-15:
                break
        return max(0.0, 1.0 - s * math.exp(-x + a * math.log(x) - math.lgamma(a)))
    b, c, d = x + 1 - a, 1e300, 1.0 / (x + 1 - a)
    h = d
    for i in range(1, 1000):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        d = 1e-300 if abs(d) < 1e-300 else d
        c = b + an / c
        c = 1e-300 if abs(c) < 1e-300 else c
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1) < 1e-15:
            break
    return min(1.0, math.exp(-x + a * math.log(x) - math.lgamma(a)) * h)


def chi2_uniform_p(counts: list) -> float | None:
    """Chi-square goodness-of-fit p-value against the uniform (None when empty)."""
    n = sum(counts)
    if not counts or n == 0 or len(counts) < 2:
        return None
    e = n / len(counts)
    stat = sum((c - e) ** 2 / e for c in counts)
    return _gammaincc((len(counts) - 1) / 2.0, stat / 2.0)


def _len_rank(texts: list, gi: int, skip: set) -> tuple:
    """(rank of the gold's length among the ordered options, n ordered, gold-is-longest credit with ties split)."""
    idx = [j for j in range(len(texts)) if j not in skip or j == gi]
    lens = {j: len(texts[j]) for j in idx}
    below = sum(1 for j in idx if j != gi and lens[j] < lens[gi])
    return below, len(idx)


def plan_report(sets: list, *, alpha: float = 0.01, longest_pp: float = 2.0) -> dict:
    """Pre-pilot balance check over built OptionSets (the pilot's G10 / G7 bars, measured on the option sets):
      abstain   per (k, shown) cell: abstain-gold count vs the planned share (meta["plan"]) or 1/k; exact binomial
      position  gold position per k: chi-square vs uniform
      rank      gold LENGTH rank among the non-abstain options per n: chi-square vs uniform
      longest   gold-is-longest (ties split) minus mean 1/k, in percentage points (G10 bar: within +/- 2)."""
    cells: dict = {}
    pos: dict = {}
    rank: dict = {}
    lg = [0.0, 0.0, 0]
    for s in sets:
        k = len(s.options)
        texts = [o.text for o in s.options]
        gi = s.gold_index
        pos.setdefault(k, [0] * k)[gi] += 1
        lens = [len(t) for t in texts]
        top = [j for j, x in enumerate(lens) if x == max(lens)]
        lg[0] += (1 / len(top)) if gi in top else 0.0
        lg[1] += 1 / k
        lg[2] += 1
        ab_key = s.meta.get("abstain_key")
        shown = bool(ab_key is not None and s.abstain_shown)
        is_ab = bool(s.meta.get("gold_is_abstain"))
        if ab_key is not None:
            p = s.meta.get("plan") or {}
            share = p.get("abstain_share") if p.get("show_abstain") else None
            c = cells.setdefault((k, shown), {"rows": 0, "abstain_gold": 0, "expected": 0.0})
            c["rows"] += 1
            c["abstain_gold"] += is_ab
            c["expected"] += (share if share is not None else (1 / k)) if shown else 0.0
        if not is_ab:
            skip = {j for j, o in enumerate(s.options) if o.role == "abstain"}
            r, n = _len_rank(texts, gi, skip)
            rank.setdefault(n, [0] * n)[min(r, n - 1)] += 1
    out_cells, bad = {}, []
    for (k, shown), c in sorted(cells.items()):
        p = binom_two_sided(c["abstain_gold"], c["rows"], c["expected"] / c["rows"]) if shown else None
        key = f"k{k}|shown={shown}"
        out_cells[key] = {**c, "expected": round(c["expected"], 2), "share": round(c["abstain_gold"] / c["rows"], 4),
                          "p_binom": None if p is None else round(p, 4)}
        if shown and (p is not None and p < alpha or c["abstain_gold"] / c["rows"] > 0.5):
            bad.append(key)
    pos_p = {k: chi2_uniform_p(v) for k, v in pos.items() if sum(v) >= 5 * k}
    rank_p = {n: chi2_uniform_p(v) for n, v in rank.items() if n >= 2 and sum(v) >= 5 * n}
    d = (100 * (lg[0] - lg[1]) / lg[2]) if lg[2] else None
    fails = (bad + [f"position k{k}" for k, p in pos_p.items() if p is not None and p <= alpha]
             + [f"length rank n{n}" for n, p in rank_p.items() if p is not None and p <= alpha]
             + (["longest"] if d is not None and abs(d) > longest_pp else []))
    return {"rows": lg[2], "abstain_cells": out_cells,
            "positions": {str(k): v for k, v in sorted(pos.items())},
            "positions_chi2_p": {str(k): None if p is None else round(p, 4) for k, p in sorted(pos_p.items())},
            "length_ranks": {str(n): v for n, v in sorted(rank.items())},
            "length_ranks_chi2_p": {str(n): None if p is None else round(p, 4) for n, p in sorted(rank_p.items())},
            "longest_gold_pp": None if d is None else round(d, 2), "failing": fails, "pass": not fails}
