"""dx_common: shared engine of reviewer R's devx renderers (yn2b/SPEC.md section 6, 8.1; DEVX notes in each dx_* file).

devx = 500 rows (F1, F2, F3, F5, F6, 100 each) rendered from dev_holdout-distribution latents by renderers that were
written from the latent schemas and the SPEC only (never from the training renderers' wording). Labels come only from
each family's shared decide(); reviewer R's own parse-back (text -> facts -> decide) must agree on 100% of rows.

A family module (dx_rule_chain, dx_tool_guard, dx_state_track, dx_lead_score, dx_def_literal) provides:
  KEY                         the family key (gen3_<name>)
  load()                      -> [Item]  the latents (from the family's exported devx latents) and their tiers / packs
  plan(items, rng)            -> [(Item, view dict)]  one row per latent (qkind, question kind, polarity, format, tpl)
  render(item, view, fb, rng) -> mv.RowSpec    the row (state, question, options, card) with gold from decide()
  parse(golden_row)           -> parsed facts  rebuilt from the RENDERED text only (state, question, options, card)
  relabel(parsed, golden_row) -> the gold in the row's answer space, computed by the shared decide() on the PARSED
                                 facts (never on the latent)
  project(item) / project_parsed(parsed) -> the decision-relevant facts (field-by-field equality check)

build_family() runs the plan, adds every row to a devx FamilyBuilder (mv_core checks, cards, options, grounding),
assembles each row into the golden format (the text the model reads) and re-derives its gold from that text. Any
disagreement stops the build (SPEC 8.1: 100% agreement; never filter).
CPU only, stdlib + mv_core, deterministic (seeds: SPEC 4.11 devx stream = train seed + 3e9).
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import mv_core as mv  # noqa: E402

DX_VERSION = "dx-1"
SPLIT = "devx"


# ================================================================================================ items
@dataclass
class Item:
    """One devx latent as the family exports it. facts / query are the family's own latent objects (dicts or
    dataclasses); gold0 is what the family's export recorded (checked against decide())."""
    lid: str
    tier: str
    pack: str
    kind: str                 # the family's question kind for this latent (e.g. outcome_is, may, score)
    facts: Any
    query: Any = None
    gold0: Any = None
    extra: dict = field(default_factory=dict)


# ================================================================================================ rng + seeds
def rng_for(key: str, *parts) -> random.Random:
    return mv.rng_for(key, SPLIT, "dx", *parts)


def latent_seed(key: str, lid: str) -> int:
    return mv.derive_seed(mv.split_seed(key, SPLIT), "dx-latent", lid)


# ================================================================================================ balancing
class Balancer:
    """Greedy yes/no balance over several single dimensions (SPEC 4.6 per template, renderer, format, tier, pack,
    polarity): choose(cands) returns the index of the candidate whose dims stay most balanced after adding its gold.
    A candidate is (dims: dict, yes: bool). Ties are broken by the rng."""

    def __init__(self, rng: random.Random):
        self.rng = rng
        self.c: dict = defaultdict(lambda: [0, 0])   # (dim, value) -> [yes, n]

    def cost(self, dims: dict, yes: bool) -> int:
        s = 0
        for k, v in dims.items():
            y, n = self.c[(k, v)]
            d = (y - (n - y))
            s += abs(d + (1 if yes else -1)) - abs(d)
        return s

    def choose(self, cands: list) -> int:
        costs = [self.cost(d, y) for d, y in cands]
        best = min(costs)
        top = [i for i, c in enumerate(costs) if c == best]
        return top[self.rng.randrange(len(top))] if len(top) > 1 else top[0]

    def add(self, dims: dict, yes: bool) -> None:
        for k, v in dims.items():
            self.c[(k, v)][0] += int(bool(yes))
            self.c[(k, v)][1] += 1

    def report(self) -> dict:
        out = defaultdict(dict)
        for (k, v), (y, n) in sorted(self.c.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
            out[str(k)][str(v)] = [y, n]
        return dict(out)


def balance_assign(units: list, rng: random.Random, rounds: int = 40, fixed: list | None = None) -> list:
    """Choose one candidate per unit so that yes/no gold is balanced in every (dim, value) stratum at once.
    units: [[(dims dict, yes bool), ...], ...] (the candidates of each unit); fixed: [(dims, yes)] rows already decided
    (they count, but cannot move). Greedy start, then local search that minimises the sum over strata of
    (yes - no)^2. Returns the chosen index per unit. Deterministic given the rng."""
    imb: Counter = Counter()
    for d, y in fixed or ():
        for k, v in d.items():
            imb[(k, v)] += 1 if y else -1

    def delta(d, y, sign):
        s = 0
        for k, v in d.items():
            x = imb[(k, v)]
            nx = x + sign * (1 if y else -1)
            s += nx * nx - x * x
        return s

    def apply(d, y, sign):
        for k, v in d.items():
            imb[(k, v)] += sign * (1 if y else -1)

    order = list(range(len(units)))
    rng.shuffle(order)
    choice = [None] * len(units)
    for u in order:
        cands = units[u]
        costs = [delta(d, y, +1) for d, y in cands]
        best = min(costs)
        top = [i for i, c in enumerate(costs) if c == best]
        choice[u] = top[rng.randrange(len(top))]
        apply(*cands[choice[u]], +1)
    for _ in range(rounds):
        improved = False
        rng.shuffle(order)
        for u in order:
            cands = units[u]
            cur = choice[u]
            apply(*cands[cur], -1)
            costs = [delta(d, y, +1) for d, y in cands]
            best = min(costs)
            if costs[cur] > best:
                top = [i for i, c in enumerate(costs) if c == best]
                choice[u] = top[rng.randrange(len(top))]
                improved = True
            apply(*cands[choice[u]], +1)
        if not improved:
            break
    return choice


class Rotor:
    """Even rotation over a list of surface choices (formats, templates) per stratum."""

    def __init__(self, rng: random.Random):
        self.rng = rng
        self.c: Counter = Counter()

    def pick(self, name: str, choices, stratum=()) -> Any:
        choices = list(choices)
        cnt = [self.c[(name, stratum, x)] for x in choices]
        lo = min(cnt)
        top = [x for x, n in zip(choices, cnt) if n == lo]
        x = top[self.rng.randrange(len(top))]
        self.c[(name, stratum, x)] += 1
        return x


# ================================================================================================ text helpers
MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December")
MONTH_NO = {m: i + 1 for i, m in enumerate(MONTHS)}
WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


def long_date(d: date) -> str:
    """'3 March 2026' (day month year, no weekday)."""
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def parse_long_date(s: str) -> date:
    m = re.fullmatch(r"(\d{1,2}) ([A-Z][a-z]+) (\d{4})", s.strip())
    if not m:
        raise ValueError(f"not a long date: {s!r}")
    return date(int(m.group(3)), MONTH_NO[m.group(2)], int(m.group(1)))


def day_of_2026(n: int) -> date:
    return date(2026, 1, 1) + timedelta(days=n - 1)


def doy_2026(d: date) -> int:
    return (d - date(2026, 1, 1)).days + 1


def num_text(x) -> str:
    """Exact decimal text: integers without decimals, else the shortest exact decimal (thousands commas)."""
    f = Fraction(x) if not isinstance(x, Fraction) else x
    if f.denominator == 1:
        return f"{f.numerator:,}"
    for places in range(1, 7):
        v = f * (10 ** places)
        if v.denominator == 1:
            s = mv.fmt_amount(f, places)
            return s
    raise ValueError(f"no short exact decimal for {x}")


def parse_num(s: str) -> Fraction:
    return Fraction(s.replace(",", ""))


def join_list(xs, last: str = "and") -> str:
    xs = list(xs)
    if not xs:
        return ""
    if len(xs) == 1:
        return xs[0]
    return ", ".join(xs[:-1]) + f" {last} " + xs[-1]


def split_list(s: str, last: str = "and") -> list:
    s = s.strip()
    if f" {last} " in s:
        head, tail = s.rsplit(f" {last} ", 1)
        return [x.strip() for x in head.split(", ") if x.strip()] + [tail.strip()]
    return [x.strip() for x in s.split(", ") if x.strip()]


def article(word: str) -> str:
    return "an" if word[:1].lower() in "aeiou" else "a"


def section_split(text: str, heads: list) -> dict:
    """Split a rendered state at known heading lines (exact line match) -> {heading: body text}."""
    out, cur, buf = {}, None, []
    for line in text.split("\n"):
        if line in heads:
            if cur is not None:
                out[cur] = "\n".join(buf).strip("\n")
            cur, buf = line, []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf).strip("\n")
    return out


# ================================================================================================ build
@dataclass
class Built:
    key: str
    fb: Any
    rows: list               # raw rows (mv_core format)
    golden: list             # assembled golden rows (the model's view)
    agree: dict              # parse-back report
    plan_report: dict
    checks: dict


def golden_of(fb, raw: dict) -> dict:
    defs = fb.defs.get(raw["meta"]["defs"]) if raw["meta"]["defs"] else None
    return mv.to_golden(raw, defs)


def answer_space(g: dict, gold_yn) -> Any:
    """Map a relabel result to the golden row's gold: noul -> 1/0, else the option string."""
    if g["qtype"] == "noul":
        if isinstance(gold_yn, str):
            gold_yn = gold_yn == "yes"
        return 1 if gold_yn else 0
    return gold_yn


def build_family(mod, check_tz: bool = True, items: list | None = None, verbose: bool = False) -> Built:
    """Plan, render, add to a devx FamilyBuilder, assemble and parse back every row. Raises on any disagreement."""
    fb = mv.FamilyBuilder(mod.KEY, generator_file=mod.__file__, check_tz=check_tz)
    rng = rng_for(mod.KEY, "plan")
    items = items if items is not None else mod.load()
    planned = mod.plan(items, rng)
    rejects = Counter()
    for it, view in planned:
        L = mv.Latent(mod.KEY, it.pack, {"dx_kind": it.kind}, view.get("q"), it.lid, SPLIT,
                      latent_seed(mod.KEY, it.lid), it.tier, tuple(view.get("edge", ())))
        r = random.Random(mv.derive_seed(L.seed, "render"))
        spec = mod.render(it, view, fb, r)
        u = fb.unit(L)
        try:
            u.add(spec)
            fb.commit(u)
        except mv.Reject as e:
            rejects[e.reason] += 1
            raise RuntimeError(f"{mod.KEY} {it.lid}: mv_core rejected a devx row ({e.reason}: {e.detail})") from e
    rows = fb.rows_for("devx")
    golden = [golden_of(fb, r) for r in rows]
    by_lid = {it.lid: it for it in items}
    agree = parse_back(mod, golden, by_lid)
    if agree["disagree"] or agree["proj_mismatch"]:
        raise AssertionError(f"{mod.KEY}: parse-back disagrees: {agree['examples'][:3]}")
    checks = mv.run_checks(rows, [])
    return Built(mod.KEY, fb, rows, golden, agree, getattr(mod, "LAST_PLAN_REPORT", {}), checks)


def parse_back(mod, golden: list, by_lid: dict) -> dict:
    """SPEC 8.1 for devx: each golden row's gold re-derived from its text (parse -> shared decide on the parsed facts)
    and the parsed decision facts compared field by field with the latent's."""
    n = ok = 0
    dis, proj_bad, ex = 0, 0, []
    for g in golden:
        n += 1
        lid = g["meta"]["latent_id"]
        try:
            parsed = mod.parse(g)
            got = answer_space(g, mod.relabel(parsed, g))
        except Exception as e:  # noqa: BLE001  a parse failure is a disagreement
            dis += 1
            ex.append({"id": g["id"], "error": f"{type(e).__name__}: {e}"[:300]})
            continue
        if got != g["gold"]:
            dis += 1
            ex.append({"id": g["id"], "gold": g["gold"], "parsed_gold": got})
            continue
        pa, pb = mod.project(by_lid[lid]), mod.project_parsed(parsed)
        if pa != pb:
            proj_bad += 1
            diff = sorted(k for k in set(pa) | set(pb) if pa.get(k) != pb.get(k))
            ex.append({"id": g["id"], "projection_differs": diff[:8],
                       "a": {k: str(pa.get(k))[:200] for k in diff[:3]}, "b": {k: str(pb.get(k))[:200] for k in diff[:3]}})
            continue
        ok += 1
    return {"rows": n, "agree": ok, "disagree": dis, "proj_mismatch": proj_bad, "examples": ex[:10]}


def blind_sheet(golden: list, n: int, seed: str) -> list:
    """A stratified sample of n rows for the blind solve, WITHOUT gold: (view kind, qtype) strata in proportion."""
    rng = random.Random(int(hashlib.sha256(seed.encode()).hexdigest(), 16))
    by = defaultdict(list)
    for g in golden:
        by[(g["meta"]["qkind"], g["meta"]["tpl"])].append(g)
    keys = sorted(by)
    for k in keys:
        rng.shuffle(by[k])
    out, i = [], 0
    while len(out) < min(n, len(golden)):
        k = keys[i % len(keys)]
        if by[k]:
            out.append(by[k].pop())
        i += 1
        if i > 100000:
            break
    out.sort(key=lambda g: g["id"])
    return [{"id": g["id"], "qtype": g["qtype"], "state": g["state"], "card": g["card"],
             "instructions": g["instructions"], "options": g["options"]} for g in out]


def summary(rows: list) -> dict:
    c = lambda f: dict(sorted(Counter(f(r) for r in rows).items()))  # noqa: E731
    yn = [r for r in rows if r["meta"]["qkind"] in ("yn", "jb")]
    return {"rows": len(rows), "qkind": c(lambda r: r["meta"]["qkind"]), "tpl": c(lambda r: r["meta"]["tpl"]),
            "fmt": c(lambda r: r["meta"]["fmt"]), "tier": c(lambda r: r["meta"]["tier"]),
            "pack": c(lambda r: r["meta"]["pack"]), "polarity": c(lambda r: str(r["meta"]["polarity"])),
            "card_style": c(lambda r: str(r["meta"]["card_style"])), "len_bin": c(lambda r: r["meta"]["len_bin"]),
            "yes_share_yn_jb": round(sum(mv._yes(r) for r in yn) / max(1, len(yn)), 4), "n_yn_jb": len(yn)}
